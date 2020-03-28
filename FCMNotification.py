from firebase_admin import messaging

import FirebaseSetup
from Utils import TEST_RESOURCE_STR, get_teamID_from_event
from Data import Message, Team
import json

def createMessage(event):
    message = Message(event)
    data = {
        'click_action': 'FLUTTER_NOTIFICATION_CLICK',
        'description': message.description,
        'needForAction': message.needForAction,
        'address': message.address,
        'creator': message.creator,
        'sound':'src/res/raw/school_fire_alarm.mp3'
    }
    return data
def send_fcm_notification(event: dict, team: Team):
    # Currently the code uses topics instead of tokens to push notification. Not sure if that is secure and as reliable
    # The code below is for tokens
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
    test_event = json.loads(TEST_RESOURCE_STR)
    teamID = get_teamID_from_event(test_event)
    team = Team(teamID)
    send_fcm_notification(test_event, team)
