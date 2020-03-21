import FirebaseSetup
from Secrets import twilio_secrets
from Data import Message, Team
import json
from urllib import parse
from twilio.rest import Client

# brackets are holders for description and needForAction respectively
CALL_SCRIPT_URL = "https://handler.twilio.com/twiml/EH1dd19d1980e983d0ffbad12486659c20?description={}&needForAction={}"

def phone_call(event, account_sid, auth_token):
    #get teamID by digging in event dictionary
    teamIDPath = event['value']['name'].split('/')
    teamID = None
    for i, word in enumerate(teamIDPath):
        if word == 'teams':
            teamID = teamIDPath[i + 1]
            break
    else:
        raise ValueError('teamID not found in path')

    team = Team(teamID) # TODO- this string is hardcoded and I still need to read the json file
    voicePhoneNumbers = team.get_voice_phone_numbers()

    message = Message(event)
    needForAction = parse.quote(message.needForAction)
    description = parse.quote(message.description)
    client = Client(account_sid, auth_token)
    for number in voicePhoneNumbers:
        call = client.calls.create(
            # URL is for static announcement
            url=CALL_SCRIPT_URL.format(description, needForAction),
            to=number,
            from_='+14069241940'
        )
        print("Result of call", call)

def gcf_entry(event):
    FirebaseSetup.setup_firebase_gcf_environment()
    account_sid, auth_token = twilio_secrets()
    phone_call(event, account_sid, auth_token)

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
    from config import ACCOUNT_SID, AUTH_TOKEN # This will break if run from cloud
    phone_call(test_event, ACCOUNT_SID, AUTH_TOKEN)
