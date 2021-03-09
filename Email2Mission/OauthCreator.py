import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


"""
Gathers Oauth credentials for user
Output: Saves token.pickle with Oauth credentials
"""

credentials: Credentials = None
if os.path.exists('token.pickle'):
    print('Loading Credentials from File...')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)

if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Refreshing new tokens...')
        flow = InstalledAppFlow.from_client_secrets_file(
            '../../secrets/client_secret.json',
            scopes=['https://www.googleapis.com/auth/gmail.readonly']	,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob'
        )
        flow.run_local_server(
            prompt='consent',
        )
        credentials = flow.credentials

    with open('token.pickle', 'wb') as f:
        print('Saving Credentials file...')
        pickle.dump(credentials, f)