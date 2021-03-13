import unittest
import config


class ConfigTestCase(unittest.TestCase):
    def test_config(self):
        config = config.twilio_config()
        self.assertIsInstance(config, dict)
        config = config.secrets_config()
        self.assertIsInstance(config, dict)


if __name__ == '__main__':
    unittest.main()
