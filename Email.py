import json
from firebase_admin import firestore


import FirebaseSetup
from Data import Team, MyMessage
from Utils import TEST_RESOURCE_STR, get_teamID_from_event


def send_email(event: dict, team: Team):
    db = team.db
    message = MyMessage(event)
    message.uids = team.get_uids()
    email = message.get_email()
    #timestamp email
    email['timestamp']= firestore.SERVER_TIMESTAMP #SERVER_TIMESTAMP exists, not sure why IDE can't find it
    db.collection('mail').document().set(email)


if __name__ == '__main__':
    FirebaseSetup.setup_firebase_local_environment()
    test_event = json.loads(TEST_RESOURCE_STR)
    teamID = get_teamID_from_event(test_event)
    team = Team(teamID, False)
    send_email(test_event, team)