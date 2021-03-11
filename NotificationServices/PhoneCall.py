import json
from urllib import parse

from twilio.rest import Client

import FirebaseSetup
from Utils import TEST_RESOURCE_STR, get_teamID_from_event
from NotificationServices.Twilio_Config import PURCHASED_PHONE_NUMBER, CALL_SCRIPT_URL
from Data import MyMessage, Team
from Secrets import twilio_secrets


def make_phone_call(event: dict, team: Team, cloud_environment=True):
    if cloud_environment:
        account_sid, auth_token = twilio_secrets()
    else:
        from config import ACCOUNT_SID, AUTH_TOKEN  # This will break if run from cloud
        account_sid, auth_token = ACCOUNT_SID, AUTH_TOKEN

    voice_phone_numbers = team.get_voice_phone_numbers()

    message = MyMessage(event)
    need_for_action = parse.quote(message.needForAction)
    description = parse.quote(message.description)
    client = Client(account_sid, auth_token)
    result = {}
    for number in voice_phone_numbers:
        call = client.calls.create(
            # URL is for static announcement
            url=CALL_SCRIPT_URL.format(description, need_for_action),
            to=number,
            from_=PURCHASED_PHONE_NUMBER
        )
        status_str = str(call.status)
        if status_str not in result.keys():
            result[status_str] = 1
        else:
            result[status_str] += 1
    return result


if __name__ == '__main__':
    FirebaseSetup.setup_firebase_environment(local_environment=True)
    test_event = json.loads(TEST_RESOURCE_STR)
    teamID = get_teamID_from_event(test_event)
    test_team = Team(teamID, False)
    print(make_phone_call(test_event, test_team, cloud_environment=False))
