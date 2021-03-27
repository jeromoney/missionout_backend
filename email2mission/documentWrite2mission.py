"""Webhook has been received and results are written to firestore. Now create mission
 by adding document to appropiate folder


    Trigger: Document Write at /webhook
    """

import sys

sys.path.append("/Users/justin/Projects/missionout_backend")
from google.cloud import firestore
import base64
import hashlib
from google.api_core.exceptions import AlreadyExists

from database_locations import MISSION_PATH, PAGE_PATH, TEAM_PATH
from email2mission.cadpage2dict import parse_email


class Mission:
    def __init__(self, email_dict: dict, id: str, sender: str):
        assert email_dict is not None
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
        return MISSION_PATH.format(team_Id=self.teamID)


class Page:
    def __init__(self, mission: Mission, email_sender: str):
        assert mission is not None
        assert email_sender is not None
        self.creator: str = email_sender
        self.description = mission.description
        self.missionDocumentPath = PAGE_PATH.format(mission_path=mission.doc_path())
        self.needForAction = mission.needForAction
        self.onlyEditors = (
            True  # Missions initiated by email only go to the Incident Command team
        )
        self.time = firestore.SERVER_TIMESTAMP
        self.ID = mission.ID  # Using the same unique SHA1 id as mission

    def doc_path(self):
        return f"{self.missionDocumentPath}/pages"


def _google_parsing_function(request: dict):
    body_base64 = request["payload"]["body"]["data"]
    return base64.b64decode(body_base64).decode("UTF-8")


def _sendgrid_parsing_function(request: dict):
    return request["text"]


def _google_sender_parsing_function(document_dict: dict):
    headers = document_dict["payload"]["headers"]
    for header in headers:
        if header["name"] == "From":
            return header["value"]
    raise ValueError("Could not find sender of email")


def _google_team_parsing_function(document_dict: dict):
    headers = document_dict["payload"]["headers"]
    for header in headers:
        if header["name"] in ("To", "Cc"):
            to_address = header["value"]
            if "," in to_address:
                to_address = to_address.split(",")[0].strip()
            db = firestore.Client()
            docs = [
                doc
                for doc in db.collection(TEAM_PATH)
                .where("missionEmail", "array_contains", to_address)
                .stream()
            ]
            if len(docs) == 0:
                raise ValueError("Could not identify team from message")
            elif len(docs) > 1:
                raise ValueError("More than one team had the same email address")
            else:
                return docs[0].to_dict()["teamID"]
            return header["value"]
    raise ValueError("Could not find TO/CC header in email")


def documentWrite2mission(event: dict):
    # identify sender and retrieve parsing function
    db = firestore.Client()
    # I could theoretically get the data from the event, but I don't want to parse the message
    path = event["value"]["name"].split('/("default)/')[1]
    doc_ref = db.document(path)
    document_data = doc_ref.get().to_dict()
    sender = document_data["webhookSource"]
    sender_dict = {
        "WebhookSender.SENDGRID": _sendgrid_parsing_function,
        "WebhookSender.GOOGLE": _google_parsing_function,
    }
    parsing_function = sender_dict[sender]
    text_body = parsing_function(document_data)
    try:
        mission_dict = parse_email(
            text_body
        )  # cadpage2dict is the only supported format at the moment
    except ValueError as e:
        # mark document as error
        doc_ref.update({"processed": "error", "error_code": str(e)})
        return
    sender_parsing_function_dict = {
        "WebhookSender.SENDGRID": None,  # _sendgrid_sender_parsing_function,
        "WebhookSender.GOOGLE": _google_sender_parsing_function,
    }

    email_sender = sender_parsing_function_dict[sender](document_data)
    team_parsing_function_dict = {
        "WebhookSender.SENDGRID": None,  # _sendgrid_sender_parsing_function,
        "WebhookSender.GOOGLE": _google_team_parsing_function,
    }
    team_Id = team_parsing_function_dict[sender](document_data)

    # parsing function returns mission, page, and unique identifier or error.
    id = hashlib.md5("foo".encode("utf8")).hexdigest()
    # TODO Need to add something in case text body is repeated
    mission = Mission(email_dict=mission_dict, id=id, sender=team_Id)
    page = Page(mission=mission, email_sender=email_sender)
    # write data to team folder. Check for idempotency
    try:
        db.collection(mission.doc_path()).document(id).create(vars(mission))
        db.collection(page.doc_path()).document(id).create(vars(page))
    except AlreadyExists:
        print("Document already exists. Ignoring redundant message")


if __name__ == "__main__":
    foo_foo = {
        "oldValue": {},
        "updateMask": {},
        "value": {
            "createTime": "2020-02-20T22:08:29.494223Z",
            "fields": {
                "webhookSource": {"stringValue": "WebhookSender.SENDGRID"},
                "needForAction": {"stringValue": "we need kisses for the puppy"},
                "missionDocumentPath": {
                    "stringValue": "/teams/demoteam.com/missions/wIdTaPhiEOB4VZmEd2e6"
                },
                "creator": {"stringValue": "Justin Matis"},
                "description": {"stringValue": "A puppy got hurt"},
                "time": {"timestampValue": "2020-02-20T22:08:29.415Z"},
                "onlyEditors": {"booleanValue": True},
            },
            "name": 'projects/missionout/databases/("default)/webhook/Oos5jA2kzg0FTajHjEpq',
            "updateTime": "2020-02-20T22:08:29.494223Z",
        },
    }
    documentWrite2mission(foo_foo)
