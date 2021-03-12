import unittest
import Config


class ConfigTestCase(unittest.TestCase):
    def test_config(self):
        config = Config.twilio_config()
        self.assertIsInstance(config, dict)
        config = Config.secrets_config()
        self.assertIsInstance(config, dict)


if __name__ == '__main__':
    unittest.main()
