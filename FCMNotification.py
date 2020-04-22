from firebase_admin import messaging
from firebase_admin._messaging_utils import UnregisteredError

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
        'sound': 'src/res/raw/school_fire_alarm.mp3'
    }
    return data


def send_fcm_notification(event: dict, team: Team):
    #apologies for the hack below. I need to pair both tokens and the uids
    tokens = team.get_tokens()
    message = messaging.MulticastMessage(
        data=createMessage(event),
        tokens=tokens
    )
    responses = messaging.send_multicast(message)
    print(F"Sent {len(tokens)} FCM messages")
    if responses.failure_count > 0 or True:
        print('Sending broadcast message since some messages did not go through')
        message = messaging.Message(
            data=createMessage(event),
            topic=team.teamID,
        )
        message.data['description'] = 'Broadcast: ' + message.data['description']
        response = messaging.send(message)
        #clean up expired tokens.
        erroneous_tokens = [tokens[i] for i, response in enumerate(responses.responses) if isinstance(response.exception, UnregisteredError)]
        team.delete_tokens(erroneous_tokens)
    return responses


if __name__ == '__main__':
    FirebaseSetup.setup_firebase_local_environment()
    test_event = json.loads(TEST_RESOURCE_STR)
    teamID = get_teamID_from_event(test_event)
    team = Team(teamID)
    send_fcm_notification(test_event, team)
