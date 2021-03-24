import sys

sys.path.append("/Users/justin/Projects/missionout_backend")

import unittest


class ReceiveMailWebhookTestCase(unittest.TestCase):
    def test_smoke_test(self):
        import email2mission.receiveemailwebhook

        event = {
            "@type": "type.googleapis.com/google.pubsub.v1.PubsubMessage",
            "attributes": None,
            "data": "eyJlbWFpbEFkZHJlc3MiOiJtaXNzaW9uQGNoYWZmZWVjb3VudHlzYXJub3J0aC5vcmciLCJoaXN0b3J5SWQiOjQ2ODcyfQ==",
        }
        results = email2mission.receiveemailwebhook.receiveEmailWebhook(event)
        self.assertEqual(("OK", 200), results)


if __name__ == "__main__":
    unittest.main()
