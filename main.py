# Entry way for google cloud functions.
import FirebaseSetup
import UserSetup
import Utils
import warnings

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
    for function in page_functions:
        try:
            function(event, team)
        except:
            print(f"Error running ${function}. Continuing execution")


def user_setup(event: dict, _):
    """Function is the entry way for the google cloud function environment"""
    FirebaseSetup.setup_firebase_gcf_environment()
    UserSetup.user_setup(event)
