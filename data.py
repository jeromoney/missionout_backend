from google.cloud import firestore
from itertools import chain
from google.cloud.exceptions import NotFound

from cloud_config import get_config

firestore_paths = get_config("firestore_document_paths")


class MyMessage:
    def __init__(self, event):
        page = event["value"]["fields"]
        self.description = page["description"]["stringValue"]
        self.needForAction = page["needForAction"]["stringValue"]
        self.missionDocumentPath = page["missionDocumentPath"]["stringValue"]
        self.creator = page["creator"]["stringValue"]
        self.onlyEditors = page["onlyEditors"]["booleanValue"]
        assert type(self.onlyEditors) is bool
        self.uids = []

    def set_uids(self, uids: list):
        self.uids = uids

    def get_email(self):
        assert self.uids != []
        return {
            "toUids": self.uids,
            "message": {
                "subject": self.description,
                "text": f"{self.description} {self.needForAction} {self.creator}",
            },
        }


class User:
    def __init__(self, snapshot_dict: dict):
        self.uid = snapshot_dict.get("uid", None)
        self.tokens = snapshot_dict.get("tokens", [])
        self.isEditor = snapshot_dict.get("isEditor", None)
        self.enableIOSCriticalAlerts = snapshot_dict.get(
            "enableIOSCriticalAlerts", False
        )
        self.iOSCriticalAlertsVolume = snapshot_dict.get("iOSCriticalAlertsVolume", 1.0)
        self.iOSSound = snapshot_dict.get("iOSSound", None)
        self.phoneNumbers = snapshot_dict.get("phoneNumbers", [])


class Team:
    def __init__(self, teamID, editors_only):
        self.teamID = teamID
        self.editorsOnly = editors_only
        self.users = []
        self.db = firestore.Client()
        self.__init_users()

    def __init_users(self):
        docs = (
            self.db.collection(firestore_paths["users"])
            .where("teamID", "==", self.teamID)
            .get()
        )
        for doc in docs:
            user = User(doc.to_dict())
            if self.editorsOnly and user.isEditor:
                self.add_user(user)
            elif not self.editorsOnly:
                self.add_user(user)

    def get_tokens(self):
        """:return active Firebase Authentication tokens for all members in team"""
        # need to collapse all token lists to a single list
        return list(
            set(
                chain.from_iterable(
                    [user.tokens for user in self.users if user.tokens is not None]
                )
            )
        )

    def add_user(self, user):
        self.users.append(user)

    def get_voice_phone_numbers(self):
        result = []
        for user in self.users:
            result += [
                phoneNumber["phoneNumber"]
                for phoneNumber in user.phoneNumbers
                if phoneNumber["allowCalls"]
            ]
        return result

    def get_mobile_phone_numbers(self):
        result = []
        for user in self.users:
            result += [
                phoneNumber["phoneNumber"]
                for phoneNumber in user.phoneNumbers
                if phoneNumber["allowText"]
            ]
        return result

    def get_uids(self):
        return [user.uid for user in self.users if user.uid is not None]

    def delete_tokens(self, erroneous_tokens):
        # This algo is a bit slow and could be sped up
        for token in erroneous_tokens:
            for user in self.users:
                if user.tokens is not None and token in user.tokens:
                    # delete token
                    doc = self.db.collection(firestore_paths["users"]).document(
                        user.uid
                    )
                    try:
                        doc.update({"tokens": firestore.firestore.ArrayRemove([token])})
                    except NotFound:
                        pass
