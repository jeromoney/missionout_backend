from firebase_admin import firestore
from itertools import chain

from google.cloud.exceptions import NotFound


class MyMessage:
    def __init__(self, event):
        page = event['value']['fields']
        self.description = page['description']['stringValue']
        self.needForAction = page['needForAction']['stringValue']
        self.missionDocumentPath = page['missionDocumentPath']['stringValue']
        self.creator = page['creator']['stringValue']
        self.onlyEditors = page['onlyEditors']['booleanValue']
        assert (type(self.onlyEditors) is bool)
        self.uids = []

    def set_uids(self, uids: list):
        self.uids = uids

    def get_email(self):
        assert self.uids != []
        return {
            'toUids': self.uids,
            'message': {
                'subject': self.description,
                'text': F"{self.description} {self.needForAction} {self.creator}",
            }
        }


class User:
    def __init__(self, snapshot_dict: dict):
        self.uid = snapshot_dict.get('uid', None)
        self.tokens = snapshot_dict.get('tokens', None)
        self.pushyTokens = snapshot_dict.get('pushyTokens', None)
        self.isEditor = snapshot_dict.get('isEditor', None)
        self.enableIOSCriticalAlerts = snapshot_dict.get('enableIOSCriticalAlerts', False)
        self.iOSCriticalAlertsVolume = snapshot_dict.get('iOSCriticalAlertsVolume', 1.0)
        self.iOSSound = snapshot_dict.get('iOSSound', None)


class Team:
    def __init__(self, teamID, editorsOnly):
        self.teamID = teamID
        self.editorsOnly = editorsOnly
        self.users = []
        self.db = firestore.client()
        self.__init_users()
        # access all numbers in /teams/{teamID}/phoneNumbers/{phoneNumbers}
        self.mobile_numbers = []
        self.voice_phone_numbers = []
        docs = self.db.collection(f'teams/{teamID}/phoneNumbers').stream()
        for doc in docs:
            phone_number = doc.get('phoneNumber')
            if phone_number is None:
                continue
            if doc.get('allowCalls'):
                self.voice_phone_numbers.append(phone_number)
            if doc.get('allowText'):
                self.mobile_numbers.append(phone_number)

    def __init_users(self):
        docs = self.db.collection("users").where("teamID", "==", self.teamID).get()
        for doc in docs:
            user = User(doc.to_dict())
            if self.editorsOnly and user.isEditor:
                self.add_user(user)
            elif not self.editorsOnly:
                self.add_user(user)

    def get_tokens(self):
        """:return active Firebase Authentication tokens for all members in team"""
        # need to collapse all token lists to a single list
        return list(set(chain.from_iterable([user.tokens for user in self.users if user.tokens is not None])))

    def get_pushy_tokens(self):
        """:return active Pushy tokens for all members in team"""
        # need to collapse all token lists to a single list
        return list(set(chain.from_iterable([user.pushyTokens for user in self.users if user.pushyTokens is not None])))

    def add_user(self, user):
        self.users.append(user)

    def get_voice_phone_numbers(self):
        return self.voice_phone_numbers

    def get_mobile_phone_numbers(self):
        return self.mobile_numbers

    def get_uids(self):
        return [user.uid for user in self.users if user.uid is not None]

    def delete_tokens(self, erroneous_tokens):
        # This algo is a bit slow and could be sped up
        for token in erroneous_tokens:
            for user in self.users:
                if user.tokens is not None and token in user.tokens:
                    # delete token
                    doc = self.db.collection("users").document(user.uid)
                    try:
                        doc.update({'tokens': firestore.firestore.ArrayRemove([token])})
                    except NotFound:
                        pass
