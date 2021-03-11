import unittest
import FirebaseSetup
import firebase_admin


class FirebaseTestCase(unittest.TestCase):
    def test_something(self):
        app = FirebaseSetup.setup_firebase_environment()
        self.assertTrue(type(app) is firebase_admin.App)


if __name__ == '__main__':
    unittest.main()
