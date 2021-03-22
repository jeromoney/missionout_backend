import sys
sys.path.append("/Users/justin/Projects/missionout_backend")
import os
import unittest

from email2mission_app.app_utils import get_gmail_credentials, LABELS, get_label_id


class App_UtilsTestCase(unittest.TestCase):
    def test_smoketest(self):
        gmail, _ = get_gmail_credentials()
        labels = (
            gmail.users()
            .labels()
            .list(
                userId=os.environ["mission_email"],
            )
            .execute()
        )
        hardcoded_label_set = set([str(dict_element) for dict_element in LABELS])
        labels_set = set([str(label) for label in labels["labels"]])
        self.assertTrue(hardcoded_label_set.issubset(labels_set))

    def test_get_label(self):
        self.assertEqual("Label_3904385370299332190", get_label_id("NewMission"))
        self.assertEqual("Label_7412520538190107930", get_label_id("ErrorMission"))
        self.assertEqual("Label_8585042744770510320", get_label_id("ProcessedMission"))


if __name__ == "__main__":
    unittest.main()
