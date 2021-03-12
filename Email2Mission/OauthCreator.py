import flask
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
import random
from datetime import datetime
import string

from Secrets import get_secret_value, set_oauth_state
import Utils
from Email2Mission import EmailUtils

"""
Gathers Oauth credentials for user
Output: Saves token.pickle with Oauth credentials
"""


def _state_generator():
    """generates a random string to ensure that only Google sends back tokens"""
    random.seed(datetime.now())
    letters = string.ascii_letters
    state = ''.join(random.choice(letters) for i in range(20))
    # store the state as a secret to later verify when Google returns a token
    set_oauth_state(state)
    return state


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
            client_secret = get_secret_value('oauth_secret')
            state = _state_generator()
            flow = Flow.from_client_config(
                client_config=client_secret,
                scopes=['https://www.googleapis.com/auth/gmail.readonly'],
                state=state
            )

            flow.redirect_uri = 'http://localhost:8080/oauth'
            authorization_url, state = flow.authorization_url(
                login_hint=get_secret_value('mission_email'),
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent',
            )
            print(authorization_url)
            return flask.redirect(authorization_url)


if __name__ == '__main__':
    Utils.set_local_environment()
    foo = oauth_creator()
    print(foo)
