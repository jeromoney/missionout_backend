import sys

sys.path.append("/Users/justin/Projects/missionout_backend")

import unittest
from firebase_setup import setup_firebase_environment
import utils


class Notification2MissionTestCase(unittest.TestCase):
    def test_smoke_test(self):
        import email2mission.notification2mission

        setup_firebase_environment()
        event = {
            "@type": "type.googleapis.com/google.pubsub.v1.PubsubMessage",
            "attributes": None,
            "data": "eyJlbWFpbEFkZHJlc3MiOiJtaXNzaW9uQGNoYWZmZWVjb3VudHlzYXJub3J0aC5vcmciLCJoaXN0b3J5SWQiOjQ2ODcyfQ==",
        }
        results = email2mission.notification2mission.notification2mission(event, None)
        # Should return something like {'historyId': '2904766', 'expiration': '1615913821664'}
        print(results)
        self.assertEqual(("OK", 200), results)


if __name__ == "__main__":
    unittest.main()
