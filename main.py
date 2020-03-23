# Entry way for google cloud functions.
import PhoneCall, TextMessage
import UserSetup


def send_page(event: dict, _):
    make_phone_call(event, _)
    make_text_message(event, _)
    #send_firebase_cloud_notification(event,_)
    #send_email(event,_)


def make_text_message(event: dict, _): # underscore is the convention for a second parameter that I don't need
    TextMessage.gcf_entry(event)

def make_phone_call(event: dict, _): # underscore is the convention for a second parameter that I don't need
    PhoneCall.gcf_entry(event)


def user_setup(event: dict, _):
    UserSetup.gcf_entry(event)
