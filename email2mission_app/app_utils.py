import sys

sys.path.append("/Users/justin/Projects/missionout_backend")

import google
import googleapiclient
from googleapiclient.discovery import build

import cloud_secrets

LABELS = [
    {"id": "Label_3904385370299332190", "name": "NewMission", "type": "user"},
    {"id": "Label_7412520538190107930", "name": "ErrorMission", "type": "user"},
    {"id": "Label_8585042744770510320", "name": "ProcessedMission", "type": "user"},
]


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
    "https://www.googleapis.com/auth/gmail.modify",
]
API_SERVICE_NAME = "gmail"
API_VERSION = "v1"


def get_label_id(label_name: str):
    results = [label["id"] for label in LABELS if label["name"] == label_name]
    if results == []:
        raise ValueError(f"Unable to find label: {label_name}")
    assert len(results) == 1
    return results[0]


def get_gmail_credentials():
    """
    Returns user's Oauth secret stashed in Google Cloud.

    Returns:
    Credentials: Gmail API access object

    """
    creds = cloud_secrets.get_secret_value("oauth_token")
    creds = google.oauth2.credentials.Credentials(**creds)
    return (
        googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, credentials=creds
        ),
        creds,
    )


if __name__ == "__main__":
    print(get_gmail_credentials())
    print(get_label_id("ErrorMission"))
    print(get_label_id("NewMission"))
