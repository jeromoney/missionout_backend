import sys
sys.path.append('/Users/justin/Projects/missionout_backend')

import google
import googleapiclient.discovery

import firebase_setup
import cloud_secrets
import config


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'


def dailypubrequest():
    """
    Trigger: Called Daily
    Subscribes emailto push notifications for incoming emails
    """
    email_address = cloud_secrets.get_secret_value('mission_email')
    creds = cloud_secrets.get_secret_value('oauth_token')
    creds = google.oauth2.credentials.Credentials(
        **creds)
    gmail = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=creds)

    request = {
        'labelIds': [config.email_2_mission_config()['labelId']],  # Label is 
        'topicName': config.email_2_mission_config()['topic']
    }
    gmail.users().stop(userId=email_address).execute()
    return gmail.users().watch(
        userId=email_address,
        body=request)\
        .execute()


if __name__ == '__main__':
    import utils
    utils.set_local_environment()
    firebase_setup.setup_firebase_environment()
    print(dailypubrequest())
