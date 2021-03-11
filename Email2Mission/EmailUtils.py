import os
import pickle
from googleapiclient.discovery import build


def get_gmail_credentials():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pickle_file = '/'.join([dir_path, 'token.pickle'])
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            creds = pickle.load(token)
    else:
        raise EnvironmentError("Authentication file missing. Have your run OauthCreator?")
    return build('gmail', 'v1', credentials=creds), creds
