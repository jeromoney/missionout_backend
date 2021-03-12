import unittest

import Secrets
import Utils


class SecretsTestCase(unittest.TestCase):
    def test_get_secrets(self):
        Utils.set_local_environment()
        result = Secrets.get_twilio_secrets()
        self.assertIsInstance(result, tuple)
        result = Secrets.get_oauth_client_secret()
        self.assertIsInstance(result, dict)
        result = Secrets.get_mission_email()
        self.assertIn("@", result)
        result = Secrets.get_oauth_token()
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
