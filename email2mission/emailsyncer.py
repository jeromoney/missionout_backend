import base64
import email
from google.cloud import firestore
import hashlib
import os

from email2mission_app.app_utils import get_gmail_credentials, get_label_id
import utils


def _set_historyId(historyId: str):
    db = firestore.Client()
    historyIdInt = int(historyId)
    document_reference = db.collection("teams").document(
        "demoteam.com"
    )  # TODO - fix hardcoding
    contents = document_reference.get()
    old_historyId = contents.get("historyId")
    if old_historyId > historyIdInt:
        raise EnvironmentError(
            f"HistoryIds are out of sequence: {old_historyId} vs {historyIdInt}"
        )
    document_reference.update({"historyId": (historyIdInt)})


def _get_historyId():
    db = firestore.Client()
    document_reference = db.collection("teams").document(
        "demoteam.com"
    )  # TODO - fix hardcoding
    contents = document_reference.get()
    return str(contents.get("historyId"))


def _get_latest_emails():
    """Returns most recent message ids of email in inbox

    Raises:
        EnvironmentError: Event is from another email address. Do not process
        EnvironmentError: No emails were retrived

    Returns:
        (list[str]): list of email ids
    """
    secret_email = os.environ["mission_email"]
    historyId = _get_historyId()
    gmail, _ = get_gmail_credentials()

    # allow while loop to execute on the first pass
    nextPageToken = None
    history_list = []
    while nextPageToken is None or nextPageToken:
        myHistory = (
            gmail.users()
            .history()
            .list(
                userId=secret_email,
                startHistoryId=historyId,
                historyTypes="messageAdded",
                labelId=get_label_id("NewMission"),
                pageToken=nextPageToken,
            )
            .execute()
        )
        new_historyId = myHistory["historyId"]
        history_list += myHistory.get("history", [])
        nextPageToken = myHistory.get("nextPageToken", False)
    if not utils.is_local_environment():
        _set_historyId(new_historyId)
    if "history" not in myHistory.keys():
        # update to latest history
        print("No emails since last sync")
        return {}
    # extract just the messageId
    messagesAdded = [
        sub_history["message"]["id"]
        for history in history_list
        for sub_history in history["messagesAdded"]
    ]
    # For testing purposes, I don't want to ratchet up the historyId

    return set(messagesAdded)


def _get_email(message_id: str):
    """Digs through the email and returns the body as plaintext

    Args:
        message (str): email message id

    Returns:
        (Email): the email body as python email object
    """
    gmail, _ = get_gmail_credentials()
    message = (
        gmail.users()
        .messages()
        .get(userId=os.environ["mission_email"], id=message_id, format="raw")
        .execute()
    )
    email_str = base64.urlsafe_b64decode(message["raw"]).decode("utf-8")
    # policy.default accesses python3 features such as get_body
    email_obj = email.message_from_string(email_str, policy=email.policy.default)
    # store id has hashed object to make sure to process emails only once
    email_obj.id = hashlib.sha1(email_str.encode("utf-8")).hexdigest()
    email_obj.message_id = message_id
    return email_obj


def get_latest_messages():
    email_ids = _get_latest_emails()
    return [_get_email(email_id) for email_id in email_ids]
