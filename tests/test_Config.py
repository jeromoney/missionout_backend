import sys

sys.path.append("/Users/justin/Projects/missionout_backend")
import unittest
import cloud_config


class Cloud_configTestCase(unittest.TestCase):
    def test_config(self):
        sys.path.append("/Users/justin/Projects/missionout_backend")
        myConfig = cloud_config.twilio_config()
        self.assertIsInstance(myConfig, dict)
        myConfig = cloud_config.secrets_config()
        self.assertIsInstance(myConfig, dict)


if __name__ == "__main__":
    unittest.main()
