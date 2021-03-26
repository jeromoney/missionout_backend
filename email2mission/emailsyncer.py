import base64
import email
from google.cloud import firestore
import hashlib
import os

from email2mission_app.app_utils import get_gmail_credentials, get_label_id
import utils

db = firestore.Client()
MAIL_CONFIG_DOCUMENT = db.collection("email_config").document(
    os.environ["mission_email"]
)


def _label_messages(message_ids: list):
    if message_ids == []:
        return
    request = {
        "ids": message_ids,
        "removeLabelIds": [get_label_id("NewMission"), "INBOX"],
        "addLabelIds": [get_label_id("ProcessedMission")],
    }
    gmail, _ = get_gmail_credentials()
    gmail.users().messages().batchModify(
        userId=os.environ["mission_email"], body=request
    ).execute()


def _set_historyId(historyId: str):
    historyIdInt = int(historyId)
    contents = MAIL_CONFIG_DOCUMENT.get()
    old_historyId = contents.get("historyId")
    if old_historyId > historyIdInt:
        raise EnvironmentError(
            f"HistoryIds are out of sequence: {old_historyId} vs {historyIdInt}"
        )
    MAIL_CONFIG_DOCUMENT.update({"historyId": (historyIdInt)})


def _get_historyId():
    contents = MAIL_CONFIG_DOCUMENT.get()
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
    if not utils.is_local_environment():
        _set_historyId(new_historyId)
        _label_messages(message_ids=messagesAdded)
    # For testing purposes, I don't want to ratchet up the historyId

    return set(messagesAdded)


def get_latest_messages():
    """Returns all emails since last sync. If an error occurs, an error is returned
    Returns:
        (dict[str:EmailMessage,ValueError]) : message id is the key and the value is either an email or an error
    """

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
            .get(userId=os.environ["mission_email"], id=message_id)
            .execute()
        )
        return message

    email_ids = _get_latest_emails()
    return {email_id: _get_email(email_id) for email_id in email_ids}
