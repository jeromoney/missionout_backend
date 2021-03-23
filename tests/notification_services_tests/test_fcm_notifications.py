import sys


sys.path.append("/Users/justin/Projects/missionout_backend")
import notification_services
import notification_services.fcm_notification
import unittest


class FCMNotificationsTestCase(unittest.TestCase):
    def test_smoketest(self):
        from utils import TEST_RESOURCE_STR, get_teamID_from_event
        import json
        from data import Team
        import sys

        sys.path.append("/Users/justin/Projects/missionout_backend")
        test_event = json.loads(TEST_RESOURCE_STR)
        teamID = get_teamID_from_event(test_event)
        myTeam = Team(teamID, False)
        result = notification_services.fcm_notification.send_fcm_notification(
            test_event, myTeam
        )
        self.assertIn("FCM", result)

if __name__ == "__main__":
    unittest.main()
