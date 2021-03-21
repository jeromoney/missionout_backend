import unittest
from data import User
from data import Team


class DataTestCase(unittest.TestCase):
    def test_something(self):
        import firebase_setup

        firebase_setup.setup_firebase_environment()

        snapshot_dict1 = {
            "voicePhoneNumber": "+17175559893",
            "mobilePhoneNumber": "+17175559893",
            "uid": "+17175559893",
            "token": "+17175559893",
        }
        snapshot_dict2 = {
            "voicePhoneNumber": "+1717123543",
            "mobilePhoneNumber": "+1717343434",
            "uid": "+171434593",
            "token": "+343435",
        }

        user1 = User(snapshot_dict1)
        user2 = User(snapshot_dict2)
        team = Team("chaffeecountysarnorth.org", editors_only=False)
        team.add_user(user1)
        team.add_user(user2)
        self.assert_(user1 in team.users)
        self.assert_(user2 in team.users)


if __name__ == "__main__":
    unittest.main()
