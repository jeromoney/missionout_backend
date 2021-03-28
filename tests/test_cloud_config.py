import sys

sys.path.append("/Users/justin/Projects/missionout_backend")
import unittest


class Cloud_configTestCase(unittest.TestCase):
    def test_basic_get(self):
        sys.path.append("/Users/justin/Projects/missionout_backend")
        import cloud_config

        result = cloud_config.get_config(module="secrets")
        self.assertIsInstance(result, dict)

    def test_missing_module(self):
        sys.path.append("/Users/justin/Projects/missionout_backend")
        import cloud_config

        with self.assertRaises(ValueError):
            cloud_config.get_config(module="foo_man_chu")

    def test_missing_file(self):
        sys.path.append("/Users/justin/Projects/missionout_backend")
        import cloud_config

        with self.assertRaises(FileNotFoundError):
            cloud_config.get_config(module="secrets", config_file="foo_man_chu.yaml")


if __name__ == "__main__":
    unittest.main()
