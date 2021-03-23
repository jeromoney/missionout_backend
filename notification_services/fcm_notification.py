from firebase_admin import messaging, firestore
from firebase_admin._messaging_utils import UnregisteredError
from firebase_admin.messaging import CriticalSound, BatchResponse
from google.cloud.firestore_v1 import WriteBatch
from google.cloud.firestore_v1.client import Client
from google.cloud import firestore
from typing import List

from utils import TEST_RESOURCE_STR, get_teamID_from_event
from data import MyMessage, Team, User
import json


class __UserTokenPair:
    def __init__(self, uid: str, token: str):
        self.uid = uid
        self.token = token


class __UserWithTokens:
    def __init__(self, uid: str, tokens: List[str]):
        self.uid = uid
        self.tokens = tokens


def __android_config():
    return messaging.AndroidConfig(
        notification=messaging.AndroidNotification(
            priority="high",
            click_action="FLUTTER_NOTIFICATION_CLICK",
            channel_id="mission_pages",
        ),
    )


def __apns_config(user: User):
    return messaging.APNSConfig(
        payload=messaging.APNSPayload(
            aps=messaging.Aps(
                content_available=True,
                sound=CriticalSound(
                    # wakey_wakey is a default option which should be installed on iOS devices
                    name=user.iOSSound
                    if user.iOSSound is not None
                    else "wakey_wakey.m4a",
                    critical=user.enableIOSCriticalAlerts,
                    volume=user.iOSCriticalAlertsVolume,
                ),
                badge=1,
            )
        )
    )


def __build_messages(user: User, data: MyMessage):
    user_messages: List[messaging.Message] = []
    for token in user.tokens:
        user_messages.append(
            messaging.Message(
                apns=__apns_config(user),
                android=__android_config(),
                notification=messaging.Notification(
                    title=data.description,
                    body=data.needForAction,
                ),
                token=token,
            )
        )
    return user_messages


def __cleanup_tokens(responses: BatchResponse, tokens: List[__UserTokenPair]):
    bad_tokens: List[__UserTokenPair] = []
    for i, response in enumerate(responses.responses):
        if not response.success:
            if type(response.exception) is UnregisteredError:
                bad_tokens.append(tokens[i])
    # for each token in the list, combine the tokens into one list
    uids = set([token.uid for token in bad_tokens])
    uid_pairs: List[__UserWithTokens] = []
    for uid in uids:
        userWithTokens = __UserWithTokens(
            uid=uid, tokens=[token.token for token in bad_tokens if token.uid == uid]
        )
        uid_pairs.append(userWithTokens)
    # delete all the tokens
    db = firestore.Client()
    assert isinstance(db, Client)
    batch = db.batch()
    assert isinstance(batch, WriteBatch)
    for uid_pair in uid_pairs:
        assert isinstance(uid_pair, __UserWithTokens)
        doc_ref = db.collection("users").document(uid_pair.uid)
        doc_ref.update({"tokens": firestore.ArrayRemove(uid_pair.tokens)})


def send_fcm_notification(event: dict, team: Team):
    import firebase_setup

    firebase_setup.setup_firebase_environment()
    messageData = MyMessage(event)
    messages: List[messaging.Message] = []
    tokens: List[__UserTokenPair] = []
    for user in team.users:
        tokens += [__UserTokenPair(uid=user.uid, token=token) for token in user.tokens]
        messages += __build_messages(user, messageData)
    responses = messaging.send_all(messages)
    __cleanup_tokens(responses, tokens)
    return f"FCM: Sent {len(responses.responses)} messages with {responses.failure_count} failures"
