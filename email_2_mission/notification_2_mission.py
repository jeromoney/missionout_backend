"""
Trigger: Push notification from pub/sub topic
Converts incoming push notification (triggered from email) and builds the appropriate document for Firestore
"""
import base64
import json
from firebase_admin import firestore

import sys
sys.path.append('/Users/justin/Projects/missionout_backend')
import firebase_setup
import cloud_secrets
import config
from email_2_mission_app.app_utils import get_gmail_credentials

MISSION_PATH = 'teams/{teamID}/missions'
PAGE_PATH = 'teams/{teamID}/missions/{missionID}/pages'


# Classes must match definition from flutter client app
class Mission:
    def __init__(self, email_dict: dict):
        self.teamID = 'demoteam.com' #TODO - fix
        self.missionID = "someIDHellosssss"
        self.description = email_dict['CALL']
        self.needForAction = email_dict['INFO']
        self.missionDocumentPath = "need this path too"
        self.time = firestore.SERVER_TIMESTAMP
        self.isStoodDown = False
        self.location = None
        self.locationDescription = email_dict['ADDR']


class Page:
    def __init__(self, mission: Mission):
        self.creator: str = "joe@blow.com" # TODO fix this
        self.description = mission.description
        self.missionDocumentPath = mission.missionDocumentPath
        self.needForAction = mission.needForAction
        self.onlyEditors = True  # Missions initiated by email only go to the Incident Command team
        self.time = firestore.SERVER_TIMESTAMP


def _get_latest_email(message_event: dict):
    """Returns most recent email in inbox"""
    emailAddress = message_event['emailAddress']
    assert emailAddress == cloud_secrets.get_secret_value('mission_email')
    historyId = message_event['historyId']
    gmail, _ = get_gmail_credentials()

    # get history ID from push notification
    myHistory = gmail.users().history().list(
        userId=emailAddress,
        startHistoryId=historyId,
        maxResults=1,
        labelId = config.email_2_mission_config()['labelId'],
    ).execute()
    messageId = myHistory['history'][0]['messages'][0]['id']
    return gmail.users().messages().get(id=messageId, userId=emailAddress).execute()


def notification2message(event, _):
    messageEvent = json.loads(base64.b64decode(event['data']))
    last_email = _get_latest_email(messageEvent)
    last_email = last_email['payload']['parts'][0]['body']['data']
    last_email = base64.b64decode(last_email).decode('UTF-8')
    import cadpage_2_dict
    email_dict = cadpage_2_dict.parse_email(last_email)
    import sys
    sys.path.append('/Users/justin/Projects/missionout_backend')
    import firebase_setup
    firebase_setup.setup_firebase_environment()
    # Build Mission from incoming email
    mission = Mission(email_dict)
    db = firestore.client()
    missionPath = MISSION_PATH.format(
        teamID=mission.teamID,
    )
    foo = db.collection(missionPath).document().set(mission.__dict__)

    # Build Page from Mission
    page = Page(mission)
    # Save to Firestore
    pagePath = PAGE_PATH.format(
        teamID=mission.teamID,
        missionID=mission.missionID
    )
    return db.collection(pagePath).document().set(page.__dict__)


if __name__ == '__main__':
    import utils
    utils.set_local_environment()
    event= {'@type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage', 'attributes': None, 'data': 'eyJlbWFpbEFkZHJlc3MiOiJtaXNzaW9uQGNoYWZmZWVjb3VudHlzYXJub3J0aC5vcmciLCJoaXN0b3J5SWQiOjQxMDkwfQ=='} 
    print(notification2message(event, None))
