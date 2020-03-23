# Entry way for google cloud functions.
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

    make_phone_call(event, team)
    send_text_message(event, team)
    send_fcm_notification(event, team)
    send_email(event, team)


def user_setup(event: dict, _):
    """Function is the entry way for the google cloud function environment"""
    FirebaseSetup.setup_firebase_gcf_environment()
    UserSetup.user_setup(event)
