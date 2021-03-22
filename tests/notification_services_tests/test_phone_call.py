import sys
import notification_services

sys.path.append("/Users/justin/Projects/missionout_backend")
import notification_services.phone_call
import unittest


class PhoneCallTestCase(unittest.TestCase):
    def test_smoketest(self):
        from utils import TEST_RESOURCE_STR, get_teamID_from_event
        import json
        from data import Team

        test_event = json.loads(TEST_RESOURCE_STR)
        teamID = get_teamID_from_event(test_event)
        test_team = Team(teamID, False)
        import sys

        sys.path.append("/Users/justin/Projects/missionout_backend")
        from notification_services.phone_call import make_phone_call
        result = make_phone_call(test_event, test_team)
        self.assertIn("Phone call result:", result)


if __name__ == "__main__":
    unittest.main()
