from firebase_admin import messaging
from firebase_admin.messaging import CriticalSound

import FirebaseSetup
from Utils import TEST_RESOURCE_STR, get_teamID_from_event
from Data import MyMessage, Team, User
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


def android_config():
    return messaging.AndroidConfig(
        notification=messaging.AndroidNotification(
            tag=NOTIFICATION_TAG,
            priority="high",
            click_action="FLUTTER_NOTIFICATION_CLICK",
            channel_id="mission_pages",
        ),
    )


def apns_config(user: User):
    return messaging.APNSConfig(
        headers={"apns-id": "345", "apns-collapse-id": "1234"},
        payload=messaging.APNSPayload(
            aps=messaging.Aps(
                content_available=True,
                sound=CriticalSound(
                    name=user.iOSSound if user.iOSSound is not None else "wakey_wakey.m4a",
                    critical=user.enableIOSCriticalAlerts,
                    volume=user.iOSCriticalAlertsVolume
                ),
                badge=1
            )
        )
    )


def build_messages(user: User, data: dict):
    user_messages = []
    for token in user.tokens:
        user_messages.append(
            messaging.Message(
                apns=apns_config(user),
                android=android_config(),
                notification=messaging.Notification(
                    title=data["description"],
                    body=data["needForAction"],
                ),
                data={"missionDocumentPath": data["missionDocumentPath"],
                      "title": data["description"],
                      "body": data["needForAction"],
                      },
                token=token
            )
        )
    return user_messages


def send_fcm_notification(event: dict, team: Team):
    # apologies for the hack below. I need to pair both tokens and the uids
    data = create_message(event)
    messages = []
    for user in team.users:
        messages += build_messages(user, data)
    responses = messaging.send_all(messages)

    # if responses.failure_count > 0:
    #     # clean up expired tokens.
    #     erroneous_tokens = [tokens[i] for i, response in enumerate(responses.responses) if
    #                         isinstance(response.exception, UnregisteredError)]
    #     team.delete_tokens(erroneous_tokens)
    return responses


if __name__ == '__main__':
    FirebaseSetup.setup_firebase_local_environment()
    test_event = json.loads(TEST_RESOURCE_STR)
    teamID = get_teamID_from_event(test_event)
    myTeam = Team(teamID, False)
    send_fcm_notification(test_event, myTeam)
