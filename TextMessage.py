#
# Send Text Messages
#
import time
import FirebaseSetup
from Secrets import twilio_secrets
from Twilio_Config import PURCHASED_PHONE_NUMBER
from Data import MyMessage, Team
import json
from twilio.rest import Client
from Utils import TEST_RESOURCE_STR, get_teamID_from_event
from datetime import datetime

DELAY = 30 # Seconds. Gives the FCM notifications a 30 second hard start before being sent. The text message notification
           # sound can overrun the louder FCM notification.
TEXT_VERSION = "3.3"


def send_text_message(event: dict, team: Team, cloud_environment=True):
    print("Running TextMessage Version", TEXT_VERSION, " - ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    time.sleep(DELAY)
    if cloud_environment:
        account_sid, auth_token = twilio_secrets()
    else:
        from config import ACCOUNT_SID, AUTH_TOKEN  # This will break if run from cloud
        account_sid, auth_token = ACCOUNT_SID, AUTH_TOKEN

    client = Client(account_sid, auth_token)
    mobile_phone_numbers = team.get_mobile_phone_numbers()
    message = MyMessage(event)

    # These need to be generated automatically
    body = F"{team.teamID} Mission. {message.description} {message.needForAction} {message.creator}"

    for number in mobile_phone_numbers:
        text_call = client.messages.create(
            body=body,
            to=number,
            from_=PURCHASED_PHONE_NUMBER
        )
        print("Status of Text Message sent to", number, "is", text_call)


if __name__ == '__main__':  # For testing

    FirebaseSetup.setup_firebase_local_environment()
    test_event = json.loads(TEST_RESOURCE_STR)
    teamID = get_teamID_from_event(test_event)
    team = Team(teamID)
    send_text_message(test_event, team, cloud_environment=False)
    print("All done with TextMessage -", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
