# Entry way for google cloud functions.
from concurrent.futures.thread import ThreadPoolExecutor

import FirebaseSetup
import UserSetup
import Utils

from Data import Team
from TextMessage import send_text_message
from FCMNotification import send_fcm_notification
from PhoneCall import make_phone_call
from Email import send_email


def send_page(event: dict, _):
    """Function is the entry way for the google cloud function environment"""
    FirebaseSetup.setup_firebase_gcf_environment()
    teamID = Utils.get_teamID_from_event(event)
    team = Team(teamID)
    page_functions = [make_phone_call, send_text_message, send_fcm_notification, send_email]
    pool = ThreadPoolExecutor()
    futures = []
    for function in page_functions:
        futures.append(pool.submit(function, *(event, team)))
    pool.shutdown(wait=True)
    print(f"Outcome: ${futures}")


def user_setup(event: dict, _):
    """Function is the entry way for the google cloud function environment"""
    FirebaseSetup.setup_firebase_gcf_environment()
    UserSetup.user_setup(event)
