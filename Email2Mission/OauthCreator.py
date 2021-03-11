
import flask
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import google_auth_oauthlib.flow

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
            print('Refreshing new tokens...')
            flow = google_auth_oauthlib.flow.Flow.from_client_config
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                '../../secrets/client_secret.json',
                scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'])

            flow.redirect_uri = 'dfdfdfdfdfr'
            authorization_url, state = flow.authorization_url(
                login_hint="dsfsfsf@gmail.com",
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent',
            )
            return flask.redirect(authorization_url)

        # with open('token.pickle', 'wb') as f:
        #     print('Saving Credentials file...')
        #     pickle.dump(creds, f)


if __name__ == '__main__':
    oauth_creator()
