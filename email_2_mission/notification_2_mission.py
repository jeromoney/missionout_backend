"""
Trigger: Push notification from pub/sub topic
Converts incoming push notification (triggered from email) and builds the appropriate document for Firestore
"""
import base64
import json
from firebase_admin import firestore

# Classes must match definition from flutter client app
import firebase_setup
import cloud_secrets
import utils
from email_2_mission_app import app_utils

EXAMPLE_EMAIL = '''
CALL: CAR CRASH
PLACE: Wendys
ADDR: 123 HUCKLEBERRY LN
CITY: BREMERTON
ID: Some identifier for this alarm (123456) 
PRI: Internal priority level (HIGH, A, 123, etc)
DATE: CAD date (10/17/2012)
TIME: CAD time 
MAP: Map page or number: 123-456: Page 5, etc::
UNIT: UNIT1, UNIT2, etc::
INFO: Notes, data: other information
'''
PAGE_PATH = 'teams/{teamID}/missions/{missionID}/pages'


class Mission:
    def __init__(self):
        self.teamID = 'demoteam.com'
        self.missionID = 'some_mission_id'
        self.description = 'Some mission Description'
        self.needForAction = 'Some need for action'
        self.missionDocumentPath = 'some/path/where/the/mission/is'


class Page:
    def __init__(self, mission: Mission):
        self.creator: str = "joe@blow.com"
        self.description = mission.description
        self.missionDocumentPath = mission.missionDocumentPath
        self.needForAction = mission.needForAction
        self.onlyEditors = True  # Missions initiated by email only go to the Incident Command team
        self.time = firestore.SERVER_TIMESTAMP

    def to_json(self):
        return


def _parse_email(email: str):
    """Converts email body of value pairs into dictionary 

    Args:
        email (str): email body in the Cadpage format
    """
    result = email.splitlines()
    result = [line for line in result if ':' in line]
    result = [line.split(':') for line in result]
    # the fanciness with the join is in case the message has colons in it
    return {line[0].strip(): ':'.join(line[1:]).strip() for line in result}

def _get_latest_email(message_event: dict):
    """Returns most recent email in inbox"""
    emailAddress = message_event['emailAddress']
    assert emailAddress == cloud_secrets.get_secret_value('mission_email')
    historyId = message_event['historyId']
    gmail, _ = app_utils.get_gmail_credentials()

    # get history ID from push notification
    myHistory = gmail.users().history().list(
        userId=emailAddress,
        startHistoryId=historyId,
        maxResults=1,
    ).execute()
    messageId = myHistory['history'][0]['messages'][0]['id']
    return gmail.users().messages().get(id=messageId, userId=emailAddress).execute()


def notification2message(event, context):
    messageEvent = json.loads(base64.b64decode(event['data']))
    #_get_latest_email(messageEvent)
    return _parse_email(EXAMPLE_EMAIL)
    # FirebaseSetup.setup_firebase_environment()
    # # Build Mission from incoming email
    # mission = Mission()
    # # Build Page from Mission
    # page = Page(mission)
    # # Save to Firestore
    # db = firestore.client()
    # pagePath = PAGE_PATH.format(
    #     teamID=mission.teamID,
    #     missionID=mission.missionID
    # )
    # db.collection(pagePath).document().set(page.__dict__)


if __name__ == '__main__':
    import yaml
    import os

    config_file = '/'.join([os.path.dirname(__file__), 'notification_2_message.yaml'])
    config = yaml.safe_load(open(config_file))
    utils.set_local_environment()
    print(notification2message(config.get('message'), None))
