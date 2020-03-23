import json
from urllib import parse

from twilio.rest import Client

import FirebaseSetup
import Utils
from Twilio_Config import PURCHASED_PHONE_NUMBER
from Data import Message, Team
from Secrets import twilio_secrets

# brackets are holders for description and needForAction respectively
CALL_SCRIPT_URL = "https://handler.twilio.com/twiml/EH1dd19d1980e983d0ffbad12486659c20?description={}&needForAction={}"


def phone_call(event, account_sid, auth_token, team):
    voice_phone_numbers = team.get_voice_phone_numbers()

    message = Message(event)
    need_for_action = parse.quote(message.needForAction)
    description = parse.quote(message.description)
    client = Client(account_sid, auth_token)
    for number in voice_phone_numbers:
        call = client.calls.create(
            # URL is for static announcement
            url=CALL_SCRIPT_URL.format(description, need_for_action),
            to=number,
            from_=PURCHASED_PHONE_NUMBER
        )
        print("Result of call", call)


def gcf_entry(event, team):
    account_sid, auth_token = twilio_secrets()
    phone_call(event, account_sid, auth_token, team)


if __name__ == '__main__':
    FirebaseSetup.setup_firebase_local_environment()
    TEST_RESOURCE_STR = '{\"oldValue\": {}, \"updateMask\": {}, \"value\": {\"createTime\": \"2020-02-20T22:08:29.494223Z\", ' \
                        '\"fields\": {\"needForAction\": {\"stringValue\": \"we need kisses for the puppy\"}, \"address\": {' \
                        '\"stringValue\": \"wLZ6aZy6pVRBJBCkZXeu\"}, \"creator\": {\"stringValue\": \"Justin Matis\"}, ' \
                        '\"description\": {\"stringValue\": \"A puppy got hurt\"}, \"time\": {\"timestampValue\": ' \
                        '\"2020-02-20T22:08:29.415Z\"}}, \"name\": \"projects/missionout/databases/(' \
                        'default)/documents/teams/chaffeecountysarnorth.org/missions/wLZ6aZy6pVRBJBCkZXeu/pages' \
                        '/icGulF5jyDuqBMnyuD2I\", \"updateTime\": \"2020-02-20T22:08:29.494223Z\"}}'
    test_event = json.loads(TEST_RESOURCE_STR)
    from config import ACCOUNT_SID, AUTH_TOKEN  # This will break if run from cloud

    teamID = Utils.get_teamID_from_event(test_event)
    team = Team(teamID)
    phone_call(test_event, ACCOUNT_SID, AUTH_TOKEN, team)
