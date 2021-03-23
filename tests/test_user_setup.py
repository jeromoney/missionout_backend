import sys

sys.path.append("/Users/justin/Projects/missionout_backend")
from user_setup import *
import unittest


class UserSetupTest(unittest.TestCase):
    def test_smoketest(self):
        test_event = {
            "providerData": [{"providerId": "demoteam.com"}],
            "uid": "some uid",
            "displayName": "Joe Blow",
            "email": "joe.blow@chaffeecountysarnorth.org",
        }
        result = user_setup(test_event)
        self.assertIn("update_time", result)


if __name__ == "__main__":
    unittest.main()
