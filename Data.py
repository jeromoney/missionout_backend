class Message:
    def __init__(self, event):
        page = event['value']['fields']
        self.description = page['description']['stringValue']
        self.needForAction = page['needForAction']['stringValue']
        self.address = page['address']['stringValue']
        self.creator = page['creator']['stringValue']


class User:
    def __init__(self, snapshot_dict: dict):
        self.voicePhoneNumber = snapshot_dict.get('voicePhoneNumber', None)
        self.mobilePhoneNumber = snapshot_dict.get('mobilePhoneNumber', None)
        self.uid = snapshot_dict.get('uid', None)
        self.token = snapshot_dict.get('token', None)


class Team:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def get_voice_phone_numbers(self):
        return [user.voicePhoneNumber for user in self.users]

    def get_mobile_phone_numbers(self):
        return [user.mobilePhoneNumber for user in self.users]
