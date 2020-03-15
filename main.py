# Entry way for google cloud functions.
import UserSetup


def sendPage(event: dict, context):
    print('hello world')

def userSetup(event: dict, context):
    UserSetup.gcf_entry(event)