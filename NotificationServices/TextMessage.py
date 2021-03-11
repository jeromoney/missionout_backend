#
# Send Text Messages
#
import time
import FirebaseSetup
import Utils
from Secrets import twilio_secrets
from NotificationServices.Twilio_Config import PURCHASED_PHONE_NUMBER
from Data import MyMessage, Team
import json
from twilio.rest import Client
from Utils import TEST_RESOURCE_STR, get_teamID_from_event


DELAY = 30  # Seconds


def send_text_message(event: dict, team: Team):
    if not Utils.is_local_environment():
        """
        Gives the FCM notifications a 30 second head start before being sent. The text message notification sound can overrun
         the louder FCM notification.
        """
        time.sleep(DELAY)

    account_sid, auth_token = twilio_secrets()
    client = Client(account_sid, auth_token)
    mobile_phone_numbers = team.get_mobile_phone_numbers()
    message = MyMessage(event)

    body = F"{team.teamID} Mission. {message.description} {message.needForAction} {message.creator}"
    result = {}
    for number in mobile_phone_numbers:
        text_call = client.messages.create(
            body=body,
            to=number,
            from_=PURCHASED_PHONE_NUMBER,
            status_callback=None,
        )
        status_str = str(text_call.status)
        if status_str not in result.keys():
            result[status_str] = 1
        else:
            result[status_str] += 1

    return F"Text Message Status: {result}"


if __name__ == '__main__':
    Utils.set_local_environment()
    FirebaseSetup.setup_firebase_environment()
    test_event = json.loads(TEST_RESOURCE_STR)
    teamID = get_teamID_from_event(test_event)
    test_team = Team(teamID, False)
    print(send_text_message(test_event, test_team))
