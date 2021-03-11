import FirebaseSetup
import Secrets
import EmailUtils

"""
Trigger: Called Daily
Subscribes mission@chaffeecountysarnorth.org to push notifications for incoming emails
"""


def main():
    TOPIC = 'projects/missionout/topics/new_mission'

    gmail, _ = EmailUtils.get_gmail_credentials()

    request = {
        'labelIds': ['INBOX'],
        'topicName': TOPIC
    }
    gmail.users().stop(userId=Secrets.mission_email(local_environment=True)).execute()
    return gmail.users().watch(
        userId=Secrets.mission_email(local_environment=True),
        body=request
    )\
        .execute()


if __name__ == '__main__':
    FirebaseSetup.setup_firebase_local_environment()
    print(main())
