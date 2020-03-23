from firebase_admin import messaging

import FirebaseSetup
import Utils
from Data import Message, Team
import json

def createMessage(event):
    message = Message(event)
    data = {
        "click_action": "FLUTTER_NOTIFICATION_CLICK",
        'description': message.description,
        'needForAction': message.needForAction,
        'address': message.address,
        'creator': message.creator,
    }
    return data
def send_fcm_notification(event: dict, team: Team):
    # registration_tokens = getRegistrationTokens()
    # message = messaging.MulticastMessage(
    #     data=createMessage(event),
    #     tokens=registration_tokens
    # )
    #
    # response = messaging.send_multicast(message, app=default_app)

    message = messaging.Message(
        data=createMessage(event),
        topic=team.teamID,
    )
    response = messaging.send(message)

    return response

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
    teamID = Utils.get_teamID_from_event(test_event)
    team = Team(teamID)
    send_fcm_notification(test_event, team)
