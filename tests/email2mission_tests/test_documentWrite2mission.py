import sys

sys.path.append("/Users/justin/Projects/missionout_backend")
from email2mission.documentWrite2mission import *
import unittest


class DocumentWrite2MissionTestCase(unittest.TestCase):
    def test_smoke_test(self):
        self.assertEqual(True)

    def _google_parsing_function_test(self):
        _google_parsing_function(foo)


if __name__ == "__main__":
    unittest.main()
