import unittest
import firebase_setup
import firebase_admin


class FirebaseTestCase(unittest.TestCase):
    def test_firebase_setup(self):
        app = firebase_setup.setup_firebase_environment()
        self.assertTrue(type(app) is firebase_admin.App)


if __name__ == "__main__":
    unittest.main()
