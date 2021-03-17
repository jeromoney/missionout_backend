
import sys
sys.path.append('/Users/justin/Projects/missionout_backend')
import unittest
import config


class ConfigTestCase(unittest.TestCase):
    def test_config(self):
        sys.path.append('/Users/justin/Projects/missionout_backend')
        myConfig = config.twilio_config()
        self.assertIsInstance(myConfig, dict)
        myConfig = config.secrets_config()
        self.assertIsInstance(myConfig, dict)


if __name__ == '__main__':
    unittest.main()
