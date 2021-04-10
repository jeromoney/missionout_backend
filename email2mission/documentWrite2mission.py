"""Webhook has been received and results are written to firestore. Now create mission
 by adding document to appropiate folder


    Trigger: Document Write at /webhook
    """
from google.cloud import firestore
import hashlib

from cloud_config import get_config


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


def documentWrite2mission(event: dict, context):
    db = firestore.Client()
    batch = db.batch()  # writes will be added to batch object
    # I could theoretically get the data from the event, but I don't want to parse the message
    path = context.resource.split("/documents/")[1]
    doc_ref = db.document(path)
    document_data_get = doc_ref.get()
    if not document_data_get.exists:
        raise FileNotFoundError("Could not find the document that triggered function")
    document_data = document_data_get.to_dict()
    # I do not need to worry if message already has been processed. It will only generate a
    # mission on the first run through.
    sender = document_data["webhookSource"]
    sender_dict = {
        "WebhookSender.SENDGRID": _sendgrid_parsing_function,
        "WebhookSender.GOOGLE": _google_parsing_function,
    }
    parsing_function = sender_dict[sender]

    try:
        text_body = parsing_function(document_data)
    except ValueError as e:
        batch.update(doc_ref, {"processed": "error", "error_code": str(e)})
        return batch, f"found error while processing webhook: {e}"
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
