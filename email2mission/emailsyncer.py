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
            .get(userId=os.environ["mission_email"], id=message_id, format="raw")
            .execute()
        )
        email_str = base64.urlsafe_b64decode(message["raw"]).decode("utf-8")
        # policy.default accesses python3 features such as get_body
        email_obj = email.message_from_string(email_str, policy=email.policy.default)
        # store id has hashed object to make sure to process emails only once
        email_obj.id = hashlib.sha1(email_str.encode("utf-8")).hexdigest()
        email_obj.message_id = message_id
        # TODO - better validation
        sender = email_obj["To"].split("@")[0]
        if sender not in white_list:
            email_obj.sender = None
            return ValueError("Sender not in email white list")
        email_obj.sender = sender
        return email_obj

    documents = db.collection("app_setup").get()
    white_list = [doc.id for doc in documents]
    email_ids = _get_latest_emails()
    return {email_id: _get_email(email_id) for email_id in email_ids}
