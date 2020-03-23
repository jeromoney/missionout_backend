#
# Send Text Messages
#
import FirebaseSetup
from Secrets import twilio_secrets
from Twilio_Config import PURCHASED_PHONE_NUMBER
from Data import Message, Team
import json
from twilio.rest import Client
import Utils
from datetime import datetime
TEXT_VERSION = "3.2"


def text_message(event: object, account_sid: object, auth_token: object, team: object) -> object:
    client = Client(account_sid, auth_token)
    mobile_phone_numbers = team.get_mobile_phone_numbers()
    message = Message(event)

    # These need to be generated automatically
    body = F"{team.teamID} Mission. {message.description} {message.needForAction} {message.creator}"

    for number in mobile_phone_numbers:
        text_call = client.messages.create(
            body=body,
            to=number,
            from_=PURCHASED_PHONE_NUMBER
            )
        print("Status of Text Message sent to", number, "is", text_call)


def gcf_entry(event, team):   # For Google Cloud Function
    print("Running TextMessage Version", TEXT_VERSION, " - ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    FirebaseSetup.setup_firebase_gcf_environment()
    account_sid, auth_token = twilio_secrets()
    text_message(event, account_sid, auth_token, team)


if __name__ == '__main__':  # For testing
    from config import ACCOUNT_SID, AUTH_TOKEN  # This will break if run from cloud

    print("Running TextMessage Version", TEXT_VERSION, " - ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    FirebaseSetup.setup_firebase_local_environment()
    TEST_RESOURCE_STR = '{\"oldValue\": {}, \"updateMask\": {}, \"value\": {\"createTime\": \"2020-02-20T22:08:29.494223Z\", ' \
                        '\"fields\": {\"needForAction\": {\"stringValue\": \"we need kisses for the puppy\"}, \"address\": {' \
                        '\"stringValue\": \"wLZ6aZy6pVRBJBCkZXeu\"}, \"creator\": {\"stringValue\": \"Justin Matis\"}, ' \
                        '\"description\": {\"stringValue\": \"A puppy got hurt\"}, \"time\": {\"timestampValue\": ' \
                        '\"2020-02-20T22:08:29.415Z\"}}, \"name\": \"projects/missionout/databases/(' \
                        'default)/documents/teams/chaffeecountysarnorth.org/missions/wLZ6aZy6pVRBJBCkZXeu/pages' \
                        '/icGulF5jyDuqBMnyuD2I\", \"updateTime\": \"2020-02-20T22:08:29.494223Z\"}}'

    test_event = json.loads(TEST_RESOURCE_STR)
    teamID = Utils.get_teamID_from_event(test_event)
    team = Team(teamID)
    text_message(test_event, ACCOUNT_SID, AUTH_TOKEN, team)
    print("All done with TextMessage -", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
