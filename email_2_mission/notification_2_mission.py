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


PAGE_PATH = 'teams/{teamID}/missions/{missionID}/pages'


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
    _get_latest_email(messageEvent)

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
    notification2message(config.get('message'), None)
