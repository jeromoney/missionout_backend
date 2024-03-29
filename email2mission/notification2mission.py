"""
Trigger: Push notification from pub/sub topic
Converts incoming push notification (triggered from email) and builds the appropriate document for Firestore
"""

import email2mission.emailsyncer
import email2mission.emailprocesser


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

    messages_dict = email2mission.emailsyncer.get_latest_messages()
    email2mission.emailprocesser.process_emails(messages_dict)
    return "OK", 200
