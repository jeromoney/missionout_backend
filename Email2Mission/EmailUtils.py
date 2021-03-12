import os
import pickle
from googleapiclient.discovery import build

import Secrets
import Utils


def get_gmail_credentials():
    """
    Returns user's Oauth secret stashed in Google Cloud.

    Returns:
    Credentials(TODO - exact type): Gmail API access object

    Raises:
    EnvironmentError: why

    """
    foo = Secrets.get_secret_value('oauth_state')


    dir_path = os.path.dirname(os.path.realpath(__file__))
    pickle_file = '/'.join([dir_path, 'token.pickle'])
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            creds = pickle.load(token)
    else:
        raise EnvironmentError("Authentication file missing. Have your run OauthCreator?")
    return build('gmail', 'v1', credentials=creds), creds


if __name__ == '__main__':
    Utils.set_local_environment()
    get_gmail_credentials()
