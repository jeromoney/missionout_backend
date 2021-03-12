import unittest

import Secrets
import Utils


class SecretsTestCase(unittest.TestCase):
    def test_get_secrets(self):
        Utils.set_local_environment()
        twilio_secrets = Secrets.twilio_secrets()
        self.assertIsInstance(twilio_secrets, tuple)
        oauth_secret = Secrets.oauth_client_secret()
        self.assertIsInstance(oauth_secret, dict)
        mission_email = Secrets.mission_email()
        self.assertIn("@", mission_email)


if __name__ == '__main__':
    unittest.main()
