import google
import googleapiclient.discovery
import os
from google.cloud import firestore


import cloud_secrets
import cloud_config
import email2mission_app.app_utils

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
API_SERVICE_NAME = "gmail"
API_VERSION = "v1"

db = firestore.Client()
MAIL_CONFIG_DOCUMENT = db.collection("email_config").document(
    os.environ["mission_email"]
)


def dailypubrequest():
    """
    Trigger: Called Daily
    Subscribes emailto push notifications for incoming emails
    """
    email_address = os.environ["mission_email"]
    creds = cloud_secrets.get_secret_value("oauth_token")
    creds = google.oauth2.credentials.Credentials(**creds)
    gmail = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=creds
    )

    request = {
        "labelIds": [email2mission_app.app_utils.get_label_id("NewMission")],
        "topicName": cloud_config.email_2_mission_config()["topic"],
    }
    gmail.users().stop(userId=email_address).execute()
    result = gmail.users().watch(userId=email_address, body=request).execute()
    historyId = int(result["historyId"])
    contents = MAIL_CONFIG_DOCUMENT.get()
    old_historyId = contents.get("historyId")
    if old_historyId > historyId:
        print(f"HistoryIds are out of sequence: {old_historyId} vs {historyId}")
    MAIL_CONFIG_DOCUMENT.update({"historyId": max(historyId, old_historyId)})
    return result


if __name__ == "__main__":
    import sys

    sys.path.append("/Users/justin/Projects/missionout_backend")
    print(dailypubrequest())
