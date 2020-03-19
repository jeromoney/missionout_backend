# Entry way for google cloud functions.
import PhoneCall
import UserSetup


def send_page(event: dict, context):
    print(context)
    print('hello world')


def make_phone_call(event: dict, _): # underscore is the convention for a second parameter that I don't need
    PhoneCall.gcf_entry(event)


def user_setup(event: dict, _):
    UserSetup.gcf_entry(event)
