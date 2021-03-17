# Entry way for google cloud functions.
import json
from concurrent.futures.thread import ThreadPoolExecutor
import delete_user_data
import firebase_setup
import user_setup
import utils

from data import Team, MyMessage
from notification_services.text_message import send_text_message
from notification_services.fcm_notification import send_fcm_notification
from notification_services.phone_call import make_phone_call
from notification_services.email import send_email


def send_page(event: dict, _):
    firebase_setup.setup_firebase_environment() #TODO - add firebase setup to individual functions
    teamID = utils.get_teamID_from_event(event)
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
    firebase_setup.setup_firebase_environment()
    user_setup.user_setup(event)


def delete_user_data(event: dict, _):
    firebase_setup.setup_firebase_environment()
    delete_user_data.delete_user_data(event)


def main_dailypubrequest(_,__):
    import email2mission.dailypubrequest
    print(email2mission.dailypubrequest.dailypubrequest())


def main_notification2mission(event: dict, _):
    import email2mission.notification2mission
    print(email2mission.dailypubrequest.notification2mission(dict, _))


if __name__ == "__main__":
    utils.set_local_environment()
    test_event = json.loads(utils.TEST_RESOURCE_STR)
    send_page(test_event, None)
