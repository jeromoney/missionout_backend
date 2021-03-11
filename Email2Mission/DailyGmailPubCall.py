import FirebaseSetup
import Secrets
import EmailUtils
import Utils

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
    gmail.users().stop(userId=Secrets.mission_email()).execute()
    return gmail.users().watch(
        userId=Secrets.mission_email(),
        body=request
    )\
        .execute()


if __name__ == '__main__':
    Utils.set_local_environment()
    FirebaseSetup.setup_firebase_environment()
    print(main())
