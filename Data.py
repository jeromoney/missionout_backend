from firebase_admin import firestore
from itertools import chain


class MyMessage:
    def __init__(self, event):
        page = event['value']['fields']
        self.description = page['description']['stringValue']
        self.needForAction = page['needForAction']['stringValue']
        self.address = page['address']['stringValue']
        self.creator = page['creator']['stringValue']
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
        try:
            self.voicePhoneNumber = snapshot_dict['voicePhoneNumber']['phoneNumber']
        except KeyError:
            print("Phone number doesn't exist or in old format")
            self.voicePhoneNumber = None

        try:
            self.mobilePhoneNumber = snapshot_dict['mobilePhoneNumber']['phoneNumber']
        except KeyError:
            print("Phone number doesn't exist or in old format")
            self.mobilePhoneNumber = None
        self.uid = snapshot_dict.get('uid', None)
        self.tokens = snapshot_dict.get('tokens', None)


class Team:
    def __init__(self, teamID):
        self.teamID = teamID
        self.users = []
        self.db = firestore.client()
        self.__init_users()

    def __init_users(self):
        docs = self.db.collection("users").where("teamID", "==", self.teamID).get()
        for doc in docs:
            user = User(doc.to_dict())
            self.add_user(user)

    def get_tokens(self):
        """:return active Firebase Authentication tokens for all members in team"""
        # need to collapse all token lists to a single list
        return list(chain.from_iterable([user.tokens for user in self.users if user.tokens is not None]))

    def add_user(self, user):
        self.users.append(user)

    def get_voice_phone_numbers(self):
        return [user.voicePhoneNumber for user in self.users if user.voicePhoneNumber is not None and user.voicePhoneNumber is not ""]

    def get_mobile_phone_numbers(self):
        return [user.mobilePhoneNumber for user in self.users if user.mobilePhoneNumber is not None and user.mobilePhoneNumber is not ""]

    def get_uids(self):
        return [user.uid for user in self.users if user.uid is not None]

    def delete_tokens(self, erroneous_tokens):
        # This algo is a bit slow and could be sped up
        for token in erroneous_tokens:
            for user in self.users:
                if user.tokens is not None and token in user.tokens:
                    # delete token
                    doc = self.db.collection("users").document(user.uid)
                    doc.update({'tokens': firestore.firestore.ArrayRemove([token])})
