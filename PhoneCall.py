import FirebaseSetup
import json
from urllib import parse
from twilio.rest import Client
from config import ACCOUNT_SID, AUTH_TOKEN

CALL_SCRIPT_URL = "https://handler.twilio.com/twiml/EH1dd19d1980e983d0ffbad12486659c20?description={}&needForAction={}" #brackers are holders for description and needForAction respectively


def createMessage(event):
    page = event['value']['fields']
    description = page['description']['stringValue']
    needForAction = page['needForAction']['stringValue']
    address = page['address']['stringValue']
    creator = page['creator']['stringValue']

    data = {
        "click_action": "FLUTTER_NOTIFICATION_CLICK",
        'description': description,
        'needForAction': needForAction,
        'address': address,
        'creator': creator,
    }
    return data

def phone_call(event):
    data = createMessage(event)

    account_sid = ACCOUNT_SID
    auth_token = AUTH_TOKEN
    needForAction = parse.quote(data['needForAction'])
    description = parse.quote(data['description'])
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        # URL is for static announcement
        url=CALL_SCRIPT_URL.format(description, needForAction),
        to='+17199662421',
        from_='+14069241940'
    )


def gcf_entry(event):
    FirebaseSetup.setup_firebase_gcf_environment()
    phone_call(event)

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
    phone_call(test_event)