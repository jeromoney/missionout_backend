import unittest
import FirebaseSetup
import firebase_admin


class MyTestCase(unittest.TestCase):
    def test_something(self):
        app = FirebaseSetup.setup_firebase_environment(local_environment=True)
        self.assertTrue(type(app) is firebase_admin.App)


if __name__ == '__main__':
    unittest.main()
