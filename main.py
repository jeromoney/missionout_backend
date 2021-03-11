# Entry way for google cloud functions.
import json
from concurrent.futures.thread import ThreadPoolExecutor

import DeleteUserData
import FirebaseSetup
import UserSetup
import Utils

from Data import Team, MyMessage
from NotificationServices.TextMessage import send_text_message
from NotificationServices.FCMNotification import send_fcm_notification
from NotificationServices.PhoneCall import make_phone_call
from NotificationServices.Email import send_email


def send_page(event: dict, _):
    FirebaseSetup.setup_firebase_environment()
    teamID = Utils.get_teamID_from_event(event)
    message = MyMessage(event)
    team = Team(teamID, message.onlyEditors)
    page_functions = [send_fcm_notification, make_phone_call, send_text_message, send_email]
    pool = ThreadPoolExecutor()
    futures = [pool.submit(function, *(event, team)) for function in page_functions]
    pool.shutdown(wait=True)
    for future in futures:
        try:
            print(f"Outcome: {future.result()}")
        except:
            print(f"Exception: {future.exception()}")


def user_setup(event: dict, _):
    FirebaseSetup.setup_firebase_environment()
    UserSetup.user_setup(event)


def delete_user_data(event: dict, _):
    FirebaseSetup.setup_firebase_environment()
    DeleteUserData.delete_user_data(event)


def oauth_creator(event: dict, _):
    from Email2Mission import OauthCreator
    OauthCreator.oauth_creator()


if __name__ == "__main__":
    import os
    os.environ["LOCAL_ENVIRONMENT"] = 'True'
    test_event = json.loads(Utils.TEST_RESOURCE_STR)
    send_page(test_event, None)
