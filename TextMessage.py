import FirebaseSetup
from Data import Message
import json
from urllib import parse
from twilio.rest import Client
from config import ACCOUNT_SID, AUTH_TOKEN

#
# Send Text Messages
#
Version = "1.0"
print("Running Version", Version)
# brackets are holders for description and needForAction respectively
CALL_SCRIPT_URL = "https://handler.twilio.com/twiml/EH1dd19d1980e983d0ffbad12486659c20?description={}&needForAction={}"


def text_message(event):

    account_sid = ACCOUNT_SID
    auth_token = AUTH_TOKEN
    client = Client(account_sid, auth_token)

    # These need to be generated automatically
    cell_number = '+15107170201'
    from_number = '+14069241940'
    body_message = "Another missing hiker found at end of the rainbow again and again"
    text_image = "https://www.colorpsychology.org/wp-content/uploads/2017/03/rainbow-symbolism.jpg"

    text_call = client.messages.create(
        to=cell_number,
        from_=from_number,
        body=body_message,
        media_url=text_image,
    )
    print("Status of Text Call", text_call)

def gcf_entry(event):
    FirebaseSetup.setup_firebase_gcf_environment()
    text_message(event)


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
    text_message(test_event)
