from firebase_admin import firestore


class Message:
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
        self.voicePhoneNumber = snapshot_dict.get('voicePhoneNumber', None)
        self.mobilePhoneNumber = snapshot_dict.get('mobilePhoneNumber', None)
        self.uid = snapshot_dict.get('uid', None)
        self.token = snapshot_dict.get('token', None)


class Team:
    def __init__(self, teamID):
        self.teamID = teamID
        self.users = []
        self.__init_users()

    def __init_users(self):
        db = firestore.client()
        docs = db.collection("users").where("teamID", "==", self.teamID).get()
        for doc in docs:
            user = User(doc.to_dict())
            self.add_user(user)

    def get_tokens(self):
        ''':return active tokens for all members in team'''
        pass

    def add_user(self, user):
        self.users.append(user)

    def get_voice_phone_numbers(self):
        return [user.voicePhoneNumber for user in self.users if user.voicePhoneNumber is not None]

    def get_mobile_phone_numbers(self):
        return [user.mobilePhoneNumber for user in self.users if user.mobilePhoneNumber is not None]

    def get_uids(self):
        return [user.uid for user in self.users if user.uid is not None]
