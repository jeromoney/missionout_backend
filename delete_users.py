import firebase_setup
from firebase_admin import auth
import re


def get_anonymous_users():
    list_users = auth.list_users()
    return [user for user in list_users.users if not user.email_verified]


def get_apple_users():
    list_users = auth.list_users()
    return [
        user
        for user in list_users.users
        if len(user.provider_data) == 1
        and user.provider_data[0].provider_id == "apple.com"
    ]


def get_google_test_users():
    list_users = auth.list_users()
    return [
        user
        for user in list_users.users
        if re.search("[a-z]*\.[0-9]{5}@gmail.com", user.email) is not None
    ]


def get_email_users():
    list_users = auth.list_users()
    return [
        user
        for user in list_users.users
        if len(user.provider_data) == 1
        and user.provider_data[0].provider_id == "password"
    ]


if __name__ == "__main__":
    firebase_setup.setup_firebase_environment()
    anonymous_users = get_anonymous_users()
    # for user in anonymous_users:
    #    auth.delete_user(user.uid)
    # google_test_users = get_google_test_users()
    # for user in google_test_users:
    #    auth.delete_user(user.uid)
    email_users = get_email_users()
    for user in email_users:
        auth.delete_user(user.uid)
