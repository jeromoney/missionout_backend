import sys

sys.path.append("/Users/justin/Projects/missionout_backend")
import unittest
from delete_users import *


class DeleteUserTestCase(unittest.TestCase):
    def test_smoketest(self):
        anonymous_list = get_anonymous_users()
        self.assertIsInstance(anonymous_list, list)
        apple_list = get_apple_users()
        self.assertIsInstance(apple_list, list)
        email_list = get_email_users()
        self.assertIsInstance(email_list, list)
        google_test = get_google_test_users()
        self.assertIsInstance(google_test, list)


if __name__ == "__main__":
    unittest.main()
