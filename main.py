# Entry way for google cloud functions.
import FirebaseSetup
import PhoneCall, TextMessage
import UserSetup
import Utils
from Data import Team


def send_page(event: dict, _):
    FirebaseSetup.setup_firebase_gcf_environment()
    teamID = Utils.get_teamID_from_event(event)
    team = Team(teamID)
    make_phone_call(event, team)
    make_text_message(event, team)
    #send_firebase_cloud_notification(event,_)
    #send_email(event,_)


def make_text_message(event: dict, team: Team): # underscore is the convention for a second parameter that I don't need
    TextMessage.gcf_entry(event, team)

def make_phone_call(event: dict, team: Team): # underscore is the convention for a second parameter that I don't need
    PhoneCall.gcf_entry(event, team)


def user_setup(event: dict, _):
    UserSetup.gcf_entry(event)
