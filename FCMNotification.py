import FirebaseSetup
from Data import Message
from firebase_admin import messaging
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

def send_fcm_notification(event):
    # registration_tokens = getRegistrationTokens()
    # message = messaging.MulticastMessage(
    #     data=createMessage(event),
    #     tokens=registration_tokens
    # )
    #
    # response = messaging.send_multicast(message, app=default_app)
    topic = 'chaffeecountysarnorth.org'

    message = messaging.Message(
        data=createMessage(event),
        topic=topic,
    )
    response = messaging.send(message)

    return response

def gcf_entry(event):
    FirebaseSetup.setup_firebase_gcf_environment()
    send_fcm_notification(event)

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
    send_fcm_notification(test_event)