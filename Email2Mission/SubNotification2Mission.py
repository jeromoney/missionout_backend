"""
Trigger: Push notification from pub/sub topic
Converts incoming push notification (triggered from email) and builds the appropriate document for Firestore
"""
import json
from firebase_admin import firestore

# Classes must match definition from flutter client app
import FirebaseSetup


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


def foo(local_environment=False):
    if local_environment:
        FirebaseSetup.setup_firebase_local_environment()
    else:
        FirebaseSetup.setup_firebase_gcf_environment()
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
    foo(local_environment=True)
