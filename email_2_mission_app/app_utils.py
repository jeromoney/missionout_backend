import google
import googleapiclient
from googleapiclient.discovery import build
from google.oauth2 import credentials

import Secrets
import Utils

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'


def get_gmail_credentials():
    """
    Returns user's Oauth secret stashed in Google Cloud.

    Returns:
    Credentials: Gmail API access object

    """
    creds = Secrets.get_secret_value('oauth_token')
    creds = google.oauth2.credentials.Credentials(
        **creds)
    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=creds), creds


if __name__ == '__main__':
    Utils.set_local_environment()
    print(get_gmail_credentials())
