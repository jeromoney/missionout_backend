import base64
import json
import email
from firebase_admin import firestore
import hashlib

import cloud_secrets
import cloud_config
from email2mission_app.app_utils import get_gmail_credentials
import firebase_setup


def _set_historyId(historyId: str):
    firebase_setup.setup_firebase_environment()
    db = firestore.client()
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
    firebase_setup.setup_firebase_environment()
    db = firestore.client()
    document_reference = db.collection("teams").document(
        "demoteam.com"
    )  # TODO - fix hardcoding
    contents = document_reference.get()
    return str(contents.get("historyId"))


def _get_latest_emails(event: dict):
    """Returns most recent message ids of email in inbox

    Args:
        event (dict): [description]

    Raises:
        EnvironmentError: Event is from another email address. Do not process
        EnvironmentError: No emails were retrived

    Returns:
        (list[str]): list of email ids
    """
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

    historyId = _get_historyId()
    gmail, _ = get_gmail_credentials()

    # get history ID from push notification
    myHistory = (
        gmail.users()
        .history()
        .list(
            userId=emailAddress,
            startHistoryId=historyId,
            historyTypes="messageAdded",
            labelId=cloud_config.email_2_mission_config()["labelId"],
        )
        .execute()
    )
    new_historyId = myHistory["historyId"]
    if "history" not in myHistory.keys():
        # update to latest history
        print("No emails since last sync")
        _set_historyId(new_historyId)
        return {}
    histories = myHistory["history"]
    # extract just the messageId
    messagesAdded = [
        sub_history["message"]["id"]
        for history in histories
        for sub_history in history["messagesAdded"]
    ]
    _set_historyId(new_historyId)
    return set(messagesAdded)


def _get_email(message: str):
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
        .get(userId="mission@chaffeecountysarnorth.org", id=message, format="raw")
        .execute()
    )
    email_str = base64.urlsafe_b64decode(message["raw"]).decode("utf-8")
    # policy.default accesses python3 features such as get_body
    email_obj = email.message_from_string(email_str, policy=email.policy.default)
    # store id has hashed object to make sure to process emails only once
    email_obj.id = hashlib.sha1(email_str.encode("utf-8")).hexdigest()
    return email_obj


def get_latest_messages(event: dict):
    email_ids = _get_latest_emails(event)
    return [_get_email(email_id) for email_id in email_ids]
