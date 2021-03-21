"""
Trigger: Push notification from pub/sub topic
Converts incoming push notification (triggered from email) and builds the appropriate document for Firestore
"""
import os

import email2mission.emailsyncer
import email2mission.emailprocesser
from email2mission_app.app_utils import get_gmail_credentials, get_label_id


def notification2mission(event, __):
    """Triggered by a push notification when an email arrives in the inbox.
     The function will process all messages since the last run

    Args:
        event ([type]): The event information is not used. The push notification
         is a signal to sync from the last stored historyId.
        The Gmail API will return the latest historyId
        __ ([type]): The context is not used

    Returns:
        (tuple): Returns acknowledgement as "OK", 200
    """

    def _label_message(message_id: str, label: str):
        request = {
            "removeLabelIds": [get_label_id("NewMission")],
            "addLabelIds": [get_label_id(label)],
        }
        gmail.users().messages().modify(
            userId=os.environ["mission_email"], id=message_id, body=request
        ).execute()

    messages = email2mission.emailsyncer.get_latest_messages()
    gmail, _ = get_gmail_credentials()
    for message in messages:
        try:
            email2mission.emailprocesser.process_email(message)
            print(f"processed: {message['from']}")
            _label_message(message_id=message.message_id, label="ProcessedMission")
        except ValueError as error:
            print(f"Error processing email: {error}")
            _label_message(message_id=message.message_id, label="ErrorMission")

    return "OK", 200
