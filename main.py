# Entry way for google cloud functions.
import json
from concurrent.futures.thread import ThreadPoolExecutor

import delete_user_data as my_delete_user_data
import user_setup as my_user_setup
import utils
from data import Team, MyMessage
from notification_services.text_message import send_text_message
from notification_services.fcm_notification import send_fcm_notification
from notification_services.phone_call import make_phone_call
from notification_services.send_email import send_email

# make sure environment variables are place
from os import environ

if environ.get("mission_email") is None:
    raise ValueError("mission_email environment variable not set")


def send_page(event: dict, _):
    teamID = utils.get_teamID_from_event(event)
    message = MyMessage(event)
    team = Team(teamID, message.onlyEditors)
    page_functions = [
        send_fcm_notification,
        make_phone_call,
        send_text_message,
        send_email,
    ]
    pool = ThreadPoolExecutor()
    futures = [pool.submit(function, *(event, team)) for function in page_functions]
    pool.shutdown(wait=True)
    for future in futures:
        try:
            print(f"Outcome: {future.result()}")
        except:
            print(f"Exception: {future.exception()}")


def user_setup(event: dict, _):
    my_user_setup.user_setup(event)


def delete_user_data(event: dict, _):
    my_delete_user_data.delete_user_data(event)


def main_dailypubrequest(_, __):
    import email2mission.dailypubrequest

    print(email2mission.dailypubrequest.dailypubrequest())


def receiveEmailWebhook(request):
    import email2mission.receiveemailwebhook

    print(request)
    print(type(request))
    return email2mission.receiveemailwebhook.receiveEmailWebhook(request)


def main_notification2mission(event: dict, _):
    import email2mission.notification2mission

    return email2mission.notification2mission.notification2mission(event, _)


def main_documentWrite2mission(event: dict, context):
    import email2mission.documentWrite2mission

    batch, message = email2mission.documentWrite2mission.documentWrite2mission(
        event, context
    )
    batch.commit()
    return message


if __name__ == "__main__":
    receiveEmailWebhook(None)