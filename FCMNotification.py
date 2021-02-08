from firebase_admin import messaging
from firebase_admin._messaging_utils import UnregisteredError
from firebase_admin.messaging import CriticalSound

import FirebaseSetup
from Utils import TEST_RESOURCE_STR, get_teamID_from_event
from Data import MyMessage, Team
import json

NOTIFICATION_TAG = "close_missionout_notification"


def create_message(event):
    message = MyMessage(event)
    data = {
        'click_action': 'FLUTTER_NOTIFICATION_CLICK',
        'description': message.description,
        'needForAction': message.needForAction,
        'missionDocumentPath': message.missionDocumentPath,
        'creator': message.creator,
    }
    return data


def send_fcm_notification(event: dict, team: Team):
    # apologies for the hack below. I need to pair both tokens and the uids
    data = create_message(event)
    tokens = team.get_tokens()
    message = messaging.MulticastMessage(
        apns=messaging.APNSConfig(
            headers={"apns-collapse-id": NOTIFICATION_TAG},
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    sound=CriticalSound(
                        name="school_fire_alarm.m4a",
                        critical=True,
                        volume=1.0
                    ),
                    badge=1
                )
            )
        ),
        android=messaging.AndroidConfig(
            notification=messaging.AndroidNotification(
                tag=NOTIFICATION_TAG,
                priority="high",
                click_action="FLUTTER_NOTIFICATION_CLICK",
                channel_id="mission_pages",
            ),
        ),
        notification=messaging.Notification(
            title=data["description"],
            body=data["needForAction"],
        ),
        data={"missionDocumentPath": data["missionDocumentPath"]},
        tokens=tokens
    )
    responses = messaging.send_multicast(message)
    print(F"Sent {len(tokens)} FCM messages")
    if responses.failure_count > 0:
        # clean up expired tokens.
        erroneous_tokens = [tokens[i] for i, response in enumerate(responses.responses) if
                            isinstance(response.exception, UnregisteredError)]
        team.delete_tokens(erroneous_tokens)
    return responses


if __name__ == '__main__':
    FirebaseSetup.setup_firebase_local_environment()
    test_event = json.loads(TEST_RESOURCE_STR)
    teamID = get_teamID_from_event(test_event)
    team = Team(teamID, False)
    send_fcm_notification(test_event, team)
