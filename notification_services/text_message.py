import time
import firebase_setup
import utils
from cloud_secrets import get_secret_value
from data import MyMessage, Team
import json
from twilio.rest import Client
from utils import TEST_RESOURCE_STR, get_teamID_from_event
import cloud_config

twilio_config = cloud_config.twilio_config()


def send_text_message(event: dict, team: Team):
    if not utils.is_local_environment():
        """
        Gives the FCM notifications a 30 second head start before being sent. The text message notification sound can overrun
         the louder FCM notification.
        """
        time.sleep(twilio_config.get("text_delay"))
    account_sid = get_secret_value("twilio_account_sid")
    auth_token = get_secret_value("twilio_auth_token")
    client = Client(account_sid, auth_token)
    mobile_phone_numbers = team.get_mobile_phone_numbers()
    message = MyMessage(event)

    body = f"{team.teamID} Mission. {message.description} {message.needForAction} {message.creator}"
    result = {}
    for number in mobile_phone_numbers:
        text_call = client.messages.create(
            body=body,
            to=number,
            from_=twilio_config.get("purchased_phone_number"),
            status_callback=None,
        )
        status_str = str(text_call.status)
        if status_str not in result.keys():
            result[status_str] = 1
        else:
            result[status_str] += 1

    return f"Text Message Status: {result}"


if __name__ == "__main__":
    firebase_setup.setup_firebase_environment()
    test_event = json.loads(TEST_RESOURCE_STR)
    teamID = get_teamID_from_event(test_event)
    test_team = Team(teamID, False)
    print(send_text_message(test_event, test_team))
