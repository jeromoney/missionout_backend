import unittest

import FirebaseSetup


class MyTestCase(unittest.TestCase):
    def test_something(self):
        from Email2Mission import DailyGmailPubCall
        FirebaseSetup.setup_firebase_environment()
        results = DailyGmailPubCall.main()
        # Should return something like {'historyId': '2904766', 'expiration': '1615913821664'}
        self.assertIn("historyId", results)


if __name__ == '__main__':
    unittest.main()
