import os
import pickle

from googleapiclient.discovery import build

import FirebaseSetup
import Secrets

"""
Trigger: Called Daily
Subscribes mission@chaffeecountysarnorth.org to push notifications for incoming emails
"""


def main():
    TOPIC = 'projects/missionout/topics/new_mission'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pickle_file = '/'.join([dir_path, 'token.pickle'])
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            creds = pickle.load(token)
    else:
        raise Exception("Authentication file missing. Have your run OauthCreator?")

    gmail = build('gmail', 'v1', credentials=creds)

    request = {
        'labelIds': ['INBOX'],
        'topicName': TOPIC
    }
    gmail.users().stop(userId=Secrets.mission_email()).execute()
    return gmail.users().watch(userId=Secrets.mission_email(), body=request).execute()


if __name__ == '__main__':
    FirebaseSetup.setup_firebase_local_environment()
    main()
