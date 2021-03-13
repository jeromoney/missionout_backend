import unittest

import firebase_setup


class MyTestCase(unittest.TestCase):
    def test_something(self):
        from email_2_mission import daily_pub_request
        firebase_setup.setup_firebase_environment()
        results = daily_pub_request.daily_pub_request()
        # Should return something like {'historyId': '2904766', 'expiration': '1615913821664'}
        self.assertIn("historyId", results)


if __name__ == '__main__':
    unittest.main()
