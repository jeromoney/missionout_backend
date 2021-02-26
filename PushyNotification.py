from pushy import PushyAPI
import Secrets

import FirebaseSetup
from Utils import TEST_RESOURCE_STR, get_teamID_from_event
from Data import MyMessage, Team
import json


def send_pushy_notification(event: dict, team: Team, cloud_environment=True):
    if cloud_environment:
        pushy_secret_api_key = Secrets.pushy_secret_api_key()
    else:
        from config import PUSHY_SECRET_API_KEY  # This will break if run from cloud
        pushy_secret_api_key = PUSHY_SECRET_API_KEY

    # Payload data you want to send to devices

    message = MyMessage(event)
    data = {"message": message.description}

    for user in team.users:
        tokens = user.pushyTokens
        if not tokens:
            continue
        # Optional push notification options (such as iOS notification fields)
        options = {
            "notification": {
                "title": message.description,
                "badge": 1,
                "sound": {
                    "name": user.iOSSound,
                    "critical": int(user.enableIOSCriticalAlerts),
                    "volume": user.iOSCriticalAlertsVolume},
                "body": message.needForAction,
            }
        }

        # Send the push notification with Pushy
        return PushyAPI.send_push_notification(data, tokens, options, pushy_secret_api_key)


if __name__ == "__main__":
    FirebaseSetup.setup_firebase_local_environment()
    test_event = json.loads(TEST_RESOURCE_STR)
    teamID = get_teamID_from_event(test_event)
    test_team = Team(teamID, False)
    print(send_pushy_notification(test_event, test_team, cloud_environment=False))