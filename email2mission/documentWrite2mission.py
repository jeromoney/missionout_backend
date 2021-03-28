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

from cloud_config import get_config
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
        return get_config(module="firestore_document_paths")["mission_path"].format(
            team_Id=self.teamID
        )


class Page:
    def __init__(self, mission: Mission, email_sender: str):
        assert mission is not None
        assert email_sender is not None
        self.creator: str = email_sender
        self.description = mission.description
        self.missionDocumentPath = mission.doc_path()
        self.needForAction = mission.needForAction
        self.onlyEditors = (
            True  # Missions initiated by email only go to the Incident Command team
        )
        self.time = firestore.SERVER_TIMESTAMP
        self.ID = mission.ID  # Using the same unique SHA1 id as mission

    def doc_path(self):
        return get_config(module="firestore_document_paths")["page_path"].format(
            mission_path=self.missionDocumentPath, mission_id=self.ID
        )


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


def _sendgrid_sender_parsing_function(document_dict: dict):
    return document_dict["from"]


def _get_team_id_from_email(to_address: str):
    """looks up email address and returns the team that it belongs to"""
    db = firestore.Client()
    docs = [
        doc
        for doc in db.collection(get_config("firestore_document_paths")["team_path"])
        .where("missionEmail", "array_contains", to_address)
        .stream()
    ]
    if len(docs) == 0:
        raise ValueError("Could not identify team from message")
    elif len(docs) > 1:
        raise ValueError("More than one team had the same email address")
    else:
        return docs[0].to_dict()["teamID"]


def _google_team_parsing_function(document_dict: dict):
    headers = document_dict["payload"]["headers"]
    for header in headers:
        if header["name"] in ("To", "Cc"):
            to_address = header["value"]
            if "," in to_address:
                to_address = to_address.split(",")[0].strip()
            return _get_team_id_from_email(to_address)

    raise ValueError("Could not find TO/CC header in email")


def _sendgrid_team_parsing_function(document_dict: dict):
    to_address = document_dict["to"]
    return _get_team_id_from_email(to_address)


def documentWrite2mission(event: dict, context):
    print(context)
    print(type(context))
    db = firestore.Client()
    batch = db.batch()  # writes will be added to batch object
    # I could theoretically get the data from the event, but I don't want to parse the message
    path = context.resource.split("/documents/")[1]
    doc_ref = db.document(path)
    document_data = doc_ref.get().to_dict()
    # I do not need to worry if message already has been processed. It will only generate a
    # mission on the first run through.
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
        batch.update(doc_ref, {"processed": "error", "error_code": str(e)})
        return batch, f"found error while processing webhook: {e}"
    sender_parsing_function_dict = {
        "WebhookSender.SENDGRID": _sendgrid_sender_parsing_function,
        "WebhookSender.GOOGLE": _google_sender_parsing_function,
    }

    email_sender = sender_parsing_function_dict[sender](document_data)
    team_parsing_function_dict = {
        "WebhookSender.SENDGRID": _sendgrid_team_parsing_function,
        "WebhookSender.GOOGLE": _google_team_parsing_function,
    }
    team_Id = team_parsing_function_dict[sender](document_data)

    # parsing function returns mission, page, and unique identifier or error.
    timeStamp: DatetimeWithNanoseconds = document_data["webhookTimestamp"]
    # theoretically if two identical missions spanned midnight, they would not be identified as duplicates
    id = hashlib.md5((f"{mission_dict}{timeStamp.date()}").encode("utf8")).hexdigest()
    mission = Mission(email_dict=mission_dict, id=id, sender=team_Id)
    page = Page(mission=mission, email_sender=email_sender)
    # write data to team folder. Check for idempotency
    existing_document = db.collection(mission.doc_path()).document(id).get()
    if existing_document.exists:
        batch.update(doc_ref, {"processed": "already exists"})
        return (
            batch,
            "Document already exists. This means the message has already been processed.",
        )

    else:
        mission_ref = db.collection(mission.doc_path()).document(id)
        batch.create(mission_ref, vars(mission))
        page_ref = db.collection(page.doc_path()).document(id)
        batch.create(page_ref, vars(page))
        batch.update(doc_ref, {"processed": "success"})
        return batch, "success"
