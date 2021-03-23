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

    def _label_messages(message_ids: list, label: str):
        if message_ids == []:
            return
        request = {
            "ids": message_ids,
            "removeLabelIds": [get_label_id("NewMission"), "INBOX"],
            "addLabelIds": [get_label_id(label)],
        }
        gmail.users().messages().batchModify(
            userId=os.environ["mission_email"], body=request
        ).execute()

    messages_dict = email2mission.emailsyncer.get_latest_messages()
    gmail, _ = get_gmail_credentials()
    good_messages = []
    bad_messages = []
    for message_id in messages_dict:
        message = messages_dict[message_id]
        if type(message) is ValueError:
            bad_messages.append(message_id)
            continue
        else:
            try:
                email2mission.emailprocesser.process_email(message)
                print(f"processed: {message['from']}")
                good_messages.append(message.message_id)
            except ValueError as error:
                print(f"Error processing email: {error}")
                bad_messages.append(message.message_id)
    _label_messages(message_ids=good_messages, label="ProcessedMission")
    _label_messages(message_ids=bad_messages, label="ErrorMission")
    return "OK", 200
