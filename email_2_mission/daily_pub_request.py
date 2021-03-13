import google
import googleapiclient.discovery

import firebase_setup
import secrets
import utils
import config


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'


def daily_pub_request():
    """
    Trigger: Called Daily
    Subscribes emailto push notifications for incoming emails
    """
    email_address = secrets.get_secret_value('mission_email')
    creds = secrets.get_secret_value('oauth_token')
    creds = google.oauth2.credentials.Credentials(
        **creds)
    gmail = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=creds)

    request = {
        'labelIds': ['INBOX'],
        'topicName': config.email_2_mission_config()['topic']
    }
    gmail.users().stop(userId=email_address).execute()
    return gmail.users().watch(
        userId=email_address,
        body=request)\
        .execute()


if __name__ == '__main__':
    utils.set_local_environment()
    firebase_setup.setup_firebase_environment()
    print(daily_pub_request())
