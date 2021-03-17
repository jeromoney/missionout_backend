"""
Trigger: Push notification from pub/sub topic
Converts incoming push notification (triggered from email) and builds the appropriate document for Firestore
"""
import base64
import json
import random
import string
from firebase_admin import firestore


import firebase_setup
import cloud_secrets
import cloud_config
from email2mission_app.app_utils import get_gmail_credentials
import email2mission.cadpage2dict



# Classes must match definition from flutter client app
class Mission:
    def __init__(self, email_dict: dict):
        self.teamID = 'demoteam.com' #TODO - fix
        self.description = email_dict['CALL']
        self.needForAction = email_dict['INFO']
        self.time = firestore.SERVER_TIMESTAMP
        self.isStoodDown = False
        self.location = None
        self.locationDescription = email_dict['ADDR']
        self.ID = _get_random_id()
    def doc_path(self):
        return f'teams/{self.teamID}/missions'


class Page:
    def __init__(self, mission: Mission):
        self.creator: str = "joe@blow.com" # TODO fix this
        self.description = mission.description
        self.missionDocumentPath = '/'.join([mission.doc_path(),mission.ID])
        self.needForAction = mission.needForAction
        self.onlyEditors = True  # Missions initiated by email only go to the Incident Command team
        self.time = firestore.SERVER_TIMESTAMP

    def doc_path(self):
        return f'{self.missionDocumentPath}/pages'
    

def _get_random_id():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(20))


def _get_latest_email(event: dict):
    """Returns most recent email in inbox"""
    message_event = json.loads(base64.b64decode(event['data']))
    emailAddress = message_event['emailAddress']
    assert emailAddress == cloud_secrets.get_secret_value('mission_email')
    historyId = message_event['historyId']
    gmail, _ = get_gmail_credentials()

    # get history ID from push notification
    myHistory = gmail.users().history().list(
        userId=emailAddress,
        startHistoryId=historyId,
        maxResults=1,
        labelId =cloud_config.email_2_mission_config()['labelId'],
    ).execute()
    messageId = myHistory['history'][0]['messages'][0]['id']
    return gmail.users().messages().get(id=messageId, userId=emailAddress).execute()


def _get_email_body(email_data: dict):
    """Digs through the email and returns the body as plaintext

    Args:
        email_data (dict): A full dictionary of an email per Gmail specs

    Returns:
        (str): the email body as plaintext
    """
    email_text = email_data['payload']['parts'][0]['body']['data']
    return  base64.b64decode(email_text).decode('UTF-8')


def notification2mission(event, _):
    print(event)
    email_data = _get_latest_email(event)
    email_text = _get_email_body(email_data)
    email_dict = email2mission.cadpage2dict.parse_email(email_text)
    firebase_setup.setup_firebase_environment()
    # Build Mission from incoming email
    mission = Mission(email_dict)
    page = Page(mission)

    db = firestore.client()
    db.collection(mission.doc_path())\
        .document(mission.ID)\
        .set(mission.__dict__)

    db.collection(page.doc_path())\
        .document()\
        .set(page.__dict__)


if __name__ == '__main__':
    import sys
    sys.path.append('/Users/justin/Projects/missionout_backend')
    import utils
    utils.set_local_environment()
    event= {'@type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage', 'attributes': None, 'data': 'eyJlbWFpbEFkZHJlc3MiOiJtaXNzaW9uQGNoYWZmZWVjb3VudHlzYXJub3J0aC5vcmciLCJoaXN0b3J5SWQiOjQxMDkwfQ=='} 
    print(notification2mission(event, None))
