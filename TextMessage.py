import FirebaseSetup
from Secrets import twilio_secrets
from Data import Message, Team
import json
from twilio.rest import Client
from datetime import datetime

#
# Send Text Messages
#


def text_message(event, account_sid, auth_token):
    client = Client(account_sid, auth_token)
    team = Team('chaffeecountysarnorth.org') # TODO- this string is hardcoded and I still need to read the json file
    voicePhoneNumbers = team.get_voice_phone_numbers()
    cellPhoneNumbers = team.get_mobile_phone_numbers()
    message = Message(event)

    # These need to be generated automatically
    cell_number = '+15106290201'
    from_number = '+14069241940'
    text_image = "https://www.colorpsychology.org/wp-content/uploads/2017/03/rainbow-symbolism.jpg"
    body = F"Chaffee County SAR Mission. {message.description} {message.needForAction} {message.creator}"
    text_call = client.messages.create(
        body=body,
        to=cell_number,
        from_=from_number,
        media_url=text_image,
    )
    print("Status of Text Call", text_call)


def gcf_entry(event):
    FirebaseSetup.setup_firebase_gcf_environment()
    account_sid, auth_token = twilio_secrets()
    text_message(event, account_sid, auth_token)


if __name__ == '__main__':
    Version = "2.0"
    print("Running TextMessage Version", Version, " - ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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

    text_message(test_event, ACCOUNT_SID, AUTH_TOKEN)
    print("All done with TextMessage -", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
