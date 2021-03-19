"""
Trigger: Push notification from pub/sub topic
Converts incoming push notification (triggered from email) and builds the appropriate document for Firestore
"""
import base64
import json
import hashlib
from firebase_admin import firestore
from google.api_core.exceptions import AlreadyExists

import firebase_setup
import cloud_secrets
import cloud_config
from email2mission_app.app_utils import get_gmail_credentials
import email2mission.cadpage2dict


# Classes must match definition from flutter client app
class Mission:
    def __init__(self, email_dict: dict, event_data: str):
        self.teamID = "demoteam.com"  # TODO - fix
        self.description = email_dict["CALL"]
        self.needForAction = email_dict["INFO"]
        self.time = firestore.SERVER_TIMESTAMP
        self.isStoodDown = False
        self.location = None
        self.locationDescription = email_dict["ADDR"]
        self.ID = _get_sha1_id(event_data)

    def doc_path(self):
        return f"teams/{self.teamID}/missions"


class Page:
    def __init__(self, mission: Mission):
        self.creator: str = "joe@blow.com"  # TODO - should be sender of message
        self.description = mission.description
        self.missionDocumentPath = "/".join([mission.doc_path(), mission.ID])
        self.needForAction = mission.needForAction
        self.onlyEditors = (
            True  # Missions initiated by email only go to the Incident Command team
        )
        self.time = firestore.SERVER_TIMESTAMP
        self.ID = mission.ID  # Using the same unique SHA1 id as mission

    def doc_path(self):
        return f"{self.missionDocumentPath}/pages"


def _get_sha1_id(event_data: str):
    """Sets document ID as sha1 digest of pubsub message. This is so repeated messages aren't processed twice.

    Args:
        event_data (str): base64 encoded message value. The values will only differ in a few places

    Returns:
        (str): Sha1 digest of message
    """
    return hashlib.sha1(event_data.encode("utf-8")).hexdigest()


def _get_latest_email(event: dict):
    """Returns most recent email in inbox"""
    event_data = event["data"]
    data_b6encoded = base64.b64decode(event_data)
    message_event = json.loads(data_b6encoded)
    # verify that the email is the missionout email address
    # This is not cryptographically secure as it's just a base64 encoded value
    # It just prevents an error a few lines down when trying to accesssing the gmail api
    emailAddress = message_event["emailAddress"]
    secret_email = cloud_secrets.get_secret_value("mission_email")
    if emailAddress != secret_email:
        raise EnvironmentError(
            f"Email address in message {emailAddress} does not match secret: {secret_email}"
        )
    historyId = message_event["historyId"]
    gmail, _ = get_gmail_credentials()

    # get history ID from push notification
    myHistory = (
        gmail.users()
        .history()
        .list(
            userId=emailAddress,
            startHistoryId=historyId,
            historyTypes="labelAdded",
            maxResults=1,
            labelId=cloud_config.email_2_mission_config()["labelId"],
        )
        .execute()
    )
    print(f"my history is: {myHistory}")
    if "history" not in myHistory.keys():
        raise EnvironmentError("No emails in history")
    messageId = myHistory["history"][0]["messages"][0]["id"]
    return gmail.users().messages().get(id=messageId, userId=emailAddress).execute()


def _get_email_body(email_data: dict):
    """Digs through the email and returns the body as plaintext

    Args:
        email_data (dict): A full dictionary of an email per Gmail specs

    Returns:
        (str): the email body as plaintext
    """
    email_text = email_data["payload"]["parts"][0]["body"]["data"]
    return base64.b64decode(email_text).decode("UTF-8")


def notification2mission(event, _):
    print(f"My event is: {event}")
    try:
        email_data = _get_latest_email(event)
        email_text = _get_email_body(email_data)
        email_dict = email2mission.cadpage2dict.parse_email(email_text)
    except EnvironmentError as error:
        print(error)
        return "OK", 200

    firebase_setup.setup_firebase_environment()
    # Build Mission from incoming email
    mission = Mission(email_dict=email_dict, event_data=event["data"])
    page = Page(mission)

    db = firestore.client()

    try:
        db.collection(mission.doc_path()).document(mission.ID).create(vars(mission))
        db.collection(page.doc_path()).document(page.ID).create(vars(page))
    except AlreadyExists:
        print("Document already exists. Duplicate message.")
        return "OK", 200

    return "OK", 200
