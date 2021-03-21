import sys

sys.path.append("/Users/justin/Projects/missionout_backend")
import unittest
import cloud_secrets


class SecretsTest(unittest.TestCase):
    def test_get_secrets(self):
        import os

        assert os.environ["mission_email"] is not None
        assert os.environ["LOCAL_ENVIRONMENT"] == "True"

        for some_key in cloud_secrets.secret_keys:
            result = cloud_secrets.get_secret_value(some_key)
            self.assertIsNotNone(result)


if __name__ == "__main__":
    import os

    assert os.environ["mission_email"] is not None
    assert os.environ["LOCAL_ENVIRONMENT"] == "True"

    unittest.main()
