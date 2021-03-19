import sys

sys.path.append("/Users/justin/Projects/missionout_backend")
import unittest
import cloud_secrets
import utils


class SecretsTest(unittest.TestCase):
    def test_get_secrets(self):
        utils.set_local_environment()
        for some_key in cloud_secrets.secret_keys:
            result = cloud_secrets.get_secret_value(some_key)
            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
