from email.message import EmailMessage
from google.api_core.exceptions import AlreadyExists
from google.cloud import firestore

import email2mission.cadpage2dict


class Mission:
    def __init__(self, email_dict: dict, id: str, sender: str):
        assert sender is not None
        assert id is not None
        self.teamID = sender
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
    def __init__(self, mission: Mission, email: EmailMessage):
        self.creator: str = email["From"]
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
    # i added some custom fields
    assert message.sender is not None
    assert message.id is not None
    message_body = message.get_body(preferencelist=["plain"])
    if message_body.get_default_type() != "text/plain":
        raise ValueError(
            f"Message body is not plain text: {message.get_default_type()}"
        )
    email_dict = email2mission.cadpage2dict.parse_email(message_body.get_payload())
    # Build Mission from incoming email
    mission = Mission(email_dict=email_dict, id=message.id, sender=message.sender)
    page = Page(mission=mission, email=message)
    db = firestore.Client()

    try:
        db.collection(mission.doc_path()).document(mission.ID).create(vars(mission))
        db.collection(page.doc_path()).document(page.ID).create(vars(page))
    except AlreadyExists:
        print("Document already exists. Duplicate message. Skipping")
        return "OK", 200