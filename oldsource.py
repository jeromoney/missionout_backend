import firebase_admin, json
from firebase_admin import credentials, firestore, messaging
from twilio.rest import Client
from config import ACCOUNT_SID, AUTH_TOKEN
import urllib.parse

from enum import Enum


class RunTimeEnvironment(Enum):
    local = 1
    hosted_deployed = 2
    hosted_debug = 3


CREDENTIALS_FILE = "credentials.json"
RESOURCE_STR = '{\"oldValue\": {}, \"updateMask\": {}, \"value\": {\"createTime\": \"2020-02-20T22:08:29.494223Z\", ' \
               '\"fields\": {\"needForAction\": {\"stringValue\": \"we need kisses for the puppy\"}, \"address\": {' \
               '\"stringValue\": \"wLZ6aZy6pVRBJBCkZXeu\"}, \"creator\": {\"stringValue\": \"Justin Matis\"}, ' \
               '\"description\": {\"stringValue\": \"A puppy got hurt\"}, \"time\": {\"timestampValue\": ' \
               '\"2020-02-20T22:08:29.415Z\"}}, \"name\": \"projects/missionout/databases/(' \
               'default)/documents/teams/chaffeecountysarnorth.org/missions/wLZ6aZy6pVRBJBCkZXeu/pages' \
               '/icGulF5jyDuqBMnyuD2I\", \"updateTime\": \"2020-02-20T22:08:29.494223Z\"}}'
RESOURCE_JSON = json.loads(RESOURCE_STR)


def getApp(runTimeEnvironment):
    if runTimeEnvironment == RunTimeEnvironment.local:
        cred = credentials.Certificate(CREDENTIALS_FILE)
        return firebase_admin.initialize_app(cred, {'databaseURL': 'https://missionout.firebaseio.com'})
    else:
        # worked in hosted debug
        if (not len(firebase_admin._apps)):
            # ensures that app hasn't already been initialized
            firebase_admin.initialize_app()
        return firebase_admin.get_app(firebase_admin._DEFAULT_APP_NAME)


def getTeamDocID():
    """
    TODO - remove hard code
    :return:
    """

    return 'chaffeecountysarnorth.org'


def getRegistrationTokens():
    """
    Queries the user collections and retrieves all tokens for a single team
    :return list of all tokens under a single team:
    """
    db = firestore.client()
    teamID = getTeamDocID()
    docs = db.collection("users").where("teamID", "==", teamID).get()
    tokens = []
    for doc in docs:
        if 'tokens' in doc._data.keys():
            tokens += doc.get('tokens')

    print(tokens)

    return tokens


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


def sendFCMMessage(default_app, event=None):
    # registration_tokens = getRegistrationTokens()
    # message = messaging.MulticastMessage(
    #     data=createMessage(event),
    #     tokens=registration_tokens
    # )
    #
    # response = messaging.send_multicast(message, app=default_app)
    topic = 'chaffeecountysarnorth.org'

    message = messaging.Message(
        data=createMessage(event),
        topic=topic,
    )
    response = messaging.send(message)

    return response


def sendText(event):
    account_sid = ACCOUNT_SID
    auth_token = AUTH_TOKEN
    client = Client(account_sid, auth_token)
    data = createMessage(event)

    message = client.messages \
        .create(
        body = F"Chaffee County SAR Mission. {data['description']} {data['needForAction']} {data['creator']}",
        from_='+14069241940',
        to='+17199662421'
    )

    print(message.sid)


def makePhoneCall(event):
    data = createMessage(event)

    account_sid = ACCOUNT_SID
    auth_token = AUTH_TOKEN
    needForAction = urllib.parse.quote(data['needForAction'])
    description = urllib.parse.quote(data['description'])
    url = F"https://handler.twilio.com/twiml/EH1dd19d1980e983d0ffbad12486659c20?description={description}&needForAction={needForAction}"
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        # URL is for static announcement
        url=url,
        to='+17199662421',
        from_='+14069241940'
    )

    print(call.sid)


def sendPage(event, context):
    """Triggered by a change to a Firestore document.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    runTimeEnvironment = None
    if event == None and context == None:  # function is local
        # code for local debugging
        runTimeEnvironment = RunTimeEnvironment.local
        event = RESOURCE_JSON
    else:
        print('Function is run in hosted environment')
        runTimeEnvironment = RunTimeEnvironment.hosted_debug
        print(event.__str__())
        print(context.__str__())

    default_app = getApp(runTimeEnvironment)

    # Send a FCM message
    print(sendFCMMessage(default_app, event))

    # Send Text
    sendText(event)

    # Make a phone call
    makePhoneCall(event)


if __name__ == '__main__':
    print(sendPage(None, None))
