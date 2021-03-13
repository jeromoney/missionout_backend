import unittest

import secrets
import utils


class SecretsTestCase(unittest.TestCase):
    def test_get_secrets(self):
        utils.set_local_environment()
        result = secrets.get_twilio_secrets()
        self.assertIsInstance(result, tuple)
        result = secrets.get_oauth_client_secret()
        self.assertIsInstance(result, dict)
        result = secrets.get_mission_email()
        self.assertIn("@", result)
        result = secrets.get_oauth_token()
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
