import unittest

from Data import User
from Data import Team



class MyTestCase(unittest.TestCase):
    def test_something(self):
        snapshot_dict1 = {
            'voicePhoneNumber' : '+17175559893',
            'mobilePhoneNumber': '+17175559893',
            'uid' : '+17175559893',
            'token': '+17175559893'}
        snapshot_dict2 = {
            'voicePhoneNumber': '+1717123543',
            'mobilePhoneNumber': '+1717343434',
            'uid': '+171434593',
            'token': '+343435'}

        user1 = User(snapshot_dict1)
        user2 = User(snapshot_dict2)
        team = Team('chaffeecountysarnorth.org')
        team.add_user(user1)
        team.add_user(user2)
        self.assert_(user1 in team.users)
        self.assert_(user2 in team.users)
        self.assert_(user1.mobilePhoneNumber in team.get_mobile_phone_numbers())
        self.assert_(user2.voicePhoneNumber in team.get_voice_phone_numbers())



if __name__ == '__main__':
    unittest.main()
