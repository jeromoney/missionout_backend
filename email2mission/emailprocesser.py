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


def process_emails(message_dict: dict):
    db = firestore.Client()
    foo = firestore.SERVER_TIMESTAMP
    batch = db.batch()
    for message_key in message_dict:
        indvidual_dict = message_dict[message_key]
        indvidual_dict["webhookTimestamp"] = firestore.SERVER_TIMESTAMP
        indvidual_dict["webhookSource"] = "WebhookSender.GOOGLE"
        message_ref = db.collection("webhook").document()
        batch.set(message_ref, indvidual_dict)
    # Commit the batch
    batch.commit()