import flask
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import google_auth_oauthlib.flow

import Secrets
import Utils
from Email2Mission import EmailUtils

"""
Gathers Oauth credentials for user
Output: Saves token.pickle with Oauth credentials
"""


def oauth_creator():
    try:
        _, creds = EmailUtils.get_gmail_credentials()
    except EnvironmentError:
        # No creds files exists
        creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print('Refreshing Access Token...')
            creds.refresh(Request())
        else:
            print('Requesting auth from user...')
            client_secret = Secrets.oauth_client_secret()
            flow = google_auth_oauthlib.flow.Flow.from_client_config(
                client_config=client_secret,
                scopes=['https://www.googleapis.com/auth/drive.metadata.readonly']
            )

            flow.redirect_uri = 'http://localhost:8080/oauth'
            authorization_url, state = flow.authorization_url(
                login_hint="dsfsfsf@gmail.com",
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent',
            )
            return flask.redirect(authorization_url)


if __name__ == '__main__':
    Utils.set_local_environment()
    oauth_creator()
