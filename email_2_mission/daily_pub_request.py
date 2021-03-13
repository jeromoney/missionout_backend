import google
import googleapiclient.discovery

import FirebaseSetup
import Secrets
import Utils
import config

"""
Trigger: Called Daily
Subscribes mission@chaffeecountysarnorth.org to push notifications for incoming emails
"""
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'


def daily_pub_request():
    email_address = Secrets.get_secret_value('mission_email')
    creds = Secrets.get_secret_value('oauth_token')
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
    Utils.set_local_environment()
    FirebaseSetup.setup_firebase_environment()
    print(daily_pub_request())
