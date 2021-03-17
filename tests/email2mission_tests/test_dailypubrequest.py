import unittest
from firebase_setup import setup_firebase_environment
import utils


class DailyPubRequestTestCase(unittest.TestCase):
    def test_smoke_test(self):
        utils.set_local_environment()
        import email2mission.dailypubrequest
        setup_firebase_environment()
        results = email2mission.dailypubrequest.dailypubrequest()
        # Should return something like {'historyId': '2904766', 'expiration': '1615913821664'}
        self.assertIn("historyId", results)


if __name__ == '__main__':
    unittest.main()
