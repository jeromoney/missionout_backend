import unittest
import sys
sys.path.append('/Users/justin/Projects/missionout_backend')
from firebase_setup import setup_firebase_environment
import utils


class DailyPubRequestTestCase(unittest.TestCase):
    def test_smoke_test(self):
        import sys
        sys.path.append('/Users/justin/Projects/missionout_backend')
        sys.path.append('/Users/justin/Projects/missionout_backend/email2mission')
        utils.set_local_environment()
        from email2mission import dailypubrequest
        setup_firebase_environment()
        results = dailypubrequest.daily_pub_request()
        # Should return something like {'historyId': '2904766', 'expiration': '1615913821664'}
        self.assertIn("historyId", results)


if __name__ == '__main__':
    unittest.main()
