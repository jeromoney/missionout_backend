from email.message import EmailMessage
from firebase_admin import firestore
from google.api_core.exceptions import AlreadyExists
import email2mission.cadpage2dict
import firebase_setup


class Mission:
    def __init__(self, email_dict: dict, id: str):
        self.teamID = "demoteam.com"  # TODO - fix
        self.description = email_dict["CALL"]
        self.needForAction = email_dict["INFO"]
        self.time = firestore.SERVER_TIMESTAMP
        self.isStoodDown = False
        self.location = None
        self.locationDescription = email_dict["ADDR"]
        self.ID = id

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


def process_email(message: EmailMessage):
    message_body = message.get_body(preferencelist=["plain"])
    if message_body.get_default_type() != "text/plain":
        raise ValueError(
            f"Message body is not plain text: {message.get_default_type()}"
        )
    email_dict = email2mission.cadpage2dict.parse_email(message_body.get_payload())
    # Build Mission from incoming email
    mission = Mission(email_dict=email_dict, id=message.id)
    page = Page(mission)
    firebase_setup.setup_firebase_environment()
    db = firestore.client()

    try:
        db.collection(mission.doc_path()).document(mission.ID).create(vars(mission))
        db.collection(page.doc_path()).document(page.ID).create(vars(page))
    except AlreadyExists:
        print("Document already exists. Duplicate message.")
        return "OK", 200