import unittest
from firebase_setup import setup_firebase_environment


class DailyPubRequestTestCase(unittest.TestCase):
    def test_smoketest(self):
        import email2mission.dailypubrequest

        setup_firebase_environment()
        results = email2mission.dailypubrequest.dailypubrequest()
        print(results)
        # Should return something like {'historyId': '2904766', 'expiration': '1615913821664'}
        self.assertIn("expiration", results.keys())


if __name__ == "__main__":
    unittest.main()
