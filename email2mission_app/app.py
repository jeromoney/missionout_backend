# -*- coding: utf-8 -*-

import os
import flask
import requests
import google.oauth2.credentials
from google_auth_oauthlib.flow import Flow
import sys
from flask import abort, Flask, request
from functools import wraps
from twilio.request_validator import RequestValidator
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum, unique, auto
from google.cloud import firestore


sys.path.append("../")
import utils
from cloud_secrets import get_secret_value, set_secret_value
import app_utils

app = flask.Flask(__name__)
app.secret_key = get_secret_value("flask_secret_key")


def validate_sendgrid_request(request):
    """Check username and password in webhook request"""
    if request.authorization:
        username = request.authorization.username
        password = request.authorization.password
        return username == os.environ.get("SENDGRID_USERNAME") and check_password_hash(
            os.environ.get("SENDGRID_PASSWORD_HASH"), password
        )
    else:
        return False


def validate_twilio_request(request):
    validator = RequestValidator(get_secret_value("twilio_auth_token"))
    return validator.validate(
        request.url, request.form, request.headers.get("X-TWILIO-SIGNATURE", "")
    )


def validate_google_request(request):
    return False


class WebhookSender(Enum):
    TWILIO = auto()
    GOOGLE = auto()
    SENDGRID = auto()


def validate_request(f):
    """Validates requests from all incoming sources"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        valididation_functions = [
            (validate_google_request, WebhookSender.GOOGLE),
            (validate_sendgrid_request, WebhookSender.SENDGRID),
        ]
        # Only one validator should pass. Returns enum if valid else returns None
        validation_status = [
            validator[1] if validator[0](request) else None
            for validator in valididation_functions
        ]
        # A list of enum that have passed the test. Should only be one
        validation_results = [
            result for result in validation_status if result is not None
        ]
        if len(validation_results) > 1:
            raise ValueError("More than one validator passed. This is my error")
        elif len(validation_results) == 1:
            return f(*args, **kwargs, validator=validation_results[0])
        else:
            return abort(403)

    return decorated_function


@app.route("/")
def index():
    return print_index_table()


@app.route("/receiveEmailWebhook", methods=["POST"])
@validate_request
def receive_email(validator: WebhookSender):
    print(request.form)

    # VALIDATE THE EVENT AND IDENTIFY IT

    # STORE THE EVENT
    webhookTimestamp = firestore.SERVER_TIMESTAMP
    item_list = [item for item in request.form.items()]
    item_dict = {item[0]: item[1] for item in item_list}
    item_dict["webhookTimestamp"] = firestore.SERVER_TIMESTAMP
    item_dict["webhookSource"] = str(validator)
    db = firestore.Client()
    db.collection(u"webhook").document().create(item_dict)
    # PROCESS THE EVENT

    return "Ok", 200


@app.route("/test")
def test_api_request():
    gmail, credentials = app_utils.get_gmail_credentials()
    labels = gmail.users().labels().list(userId=os.environ["mission_email"]).execute()

    # Save credentials back to session in case access token was refreshed.
    # TODO: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    flask.session["credentials"] = credentials_to_dict(credentials)

    return "Yes, I seem to work"


@app.route("/authorize")
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    client_secret = get_secret_value("oauth_secret")
    flow = Flow.from_client_config(
        client_config=client_secret,
        scopes=app_utils.SCOPES,
    )

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which youcloud_configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = flask.url_for("oauth2callback", _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="true",
    )

    # Store the state so the callback can verify the auth server response.
    flask.session["state"] = state

    return flask.redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session["state"]

    client_secret = get_secret_value("oauth_secret")
    flow = Flow.from_client_config(
        client_config=client_secret, scopes=app_utils.SCOPES, state=state
    )
    flow.redirect_uri = flask.url_for("oauth2callback", _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    credentials = flow.credentials
    credentials = credentials_to_dict(credentials)
    if credentials.get("refresh_token") is None:
        return "Missing refresh token. Remove MissionOut from your google account and try again"
    flask.session["credentials"] = credentials
    # TODO - allow only mission email in
    set_secret_value(key="oauth_token", value=flask.session["credentials"])
    print("Saved credentials..")
    return flask.redirect(flask.url_for("test_api_request"))


@app.route("/revoke")
def revoke():
    if "credentials" not in flask.session:
        return (
            'You need to <a href="/authorize">authorize</a> before '
            + "testing the code to revoke credentials."
        )

    credentials = google.oauth2.credentials.Credentials(**flask.session["credentials"])

    revoke_str = requests.post(
        "https://oauth2.googleapis.com/revoke",
        params={"token": credentials.token},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    status_code = getattr(revoke_str, "status_code")
    if status_code == 200:
        return "Credentials successfully revoked." + print_index_table()
    else:
        return "An error occurred." + print_index_table()


@app.route("/clear")
def clear_credentials():
    if "credentials" in flask.session:
        del flask.session["credentials"]
    return "Credentials have been cleared.<br><br>" + print_index_table()


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def print_index_table():
    return (
        "<table>"
        + '<tr><td><a href="/test">Test an API request</a></td>'
        + "<td>Submit an API request and see a formatted JSON response. "
        + "    Go through the authorization flow if there are no stored "
        + "    credentials for the user.</td></tr>"
        + '<tr><td><a href="/authorize">Test the auth flow directly</a></td>'
        + "<td>Go directly to the authorization flow. If there are stored "
        + "    credentials, you still might not be prompted to reauthorize "
        + "    the application.</td></tr>"
        + '<tr><td><a href="/revoke">Revoke current credentials</a></td>'
        + "<td>Revoke the access token associated with the current user "
        + "    session. After revoking credentials, if you go to the test "
        + "    page, you should see an <code>invalid_grant</code> error."
        + "</td></tr>"
        + '<tr><td><a href="/clear">Clear Flask session credentials</a></td>'
        + "<td>Clear the access token currently stored in the user session. "
        + '    After clearing the token, if you <a href="/test">test the '
        + "    API request</a> again, you should go back to the auth flow."
        + "</td></tr></table>"
    )


if __name__ == "__main__":
    app.secret_key = get_secret_value("flask_secret_key")

    # When running locally, disable OAuthlib's HTTPs verification.
    # TODO ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Specify a hostname and port that are set as a valid redirect URI
    # for your API project in the Google API Console.
    app.run("localhost", 8080, debug=True)
