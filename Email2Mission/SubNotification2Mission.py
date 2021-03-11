"""
Trigger: Push notification from pub/sub topic
Converts incoming push notification (triggered from email) and builds the appropriate document for Firestore
"""
import json
from firebase_admin import firestore

# Classes must match definition from flutter client app
import FirebaseSetup
import Secrets
import Utils
from Email2Mission import EmailUtils


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


def get_latest_email():
    gmail, _ = EmailUtils.get_gmail_credentials()

    # get history ID from push notification
    myHistory = gmail.users().history().list(userId="sfsfsdfsdfsf@gmail.com", startHistoryId="2905635").execute()

    foo = gmail.users().messages().get(id='178193c81c9bd9b5', userId="dfsfsdfsfs@gmail.com").execute()
    print(foo)


def foo():
    FirebaseSetup.setup_firebase_environment()
    # Build Mission from incoming email
    mission = Mission()
    # Build Page from Mission
    page = Page(mission)
    # Save to Firestore
    db = firestore.client()
    pagePath = PAGE_PATH.format(
        teamID=mission.teamID,
        missionID=mission.missionID
    )
    db.collection(pagePath).document().set(page.__dict__)


if __name__ == '__main__':
    Utils.set_local_environment()
    # foo(local_environment=True)
    get_latest_email()
