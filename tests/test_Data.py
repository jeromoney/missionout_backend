import sys


sys.path.append("/Users/justin/Projects/missionout_backend")
import unittest
from data import User
from data import Team


class DataTestCase(unittest.TestCase):
    def test_smoketest(self):

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

    def test_phone_numbers(self):
        team = Team(editors_only=True, teamID="demoteam.com")
        voice_phone_numbers = team.get_voice_phone_numbers()
        text_phone_numbers = team.get_mobile_phone_numbers()
        self.assertIsInstance(voice_phone_numbers, list)
        self.assertIsInstance(text_phone_numbers, list)


if __name__ == "__main__":
    unittest.main()
