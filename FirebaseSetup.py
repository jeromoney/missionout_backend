import firebase_admin
from firebase_admin import credentials


CREDENTIALS_FILE = "credentials.json"


def setup_firebase_local_environment():
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cred = credentials.Certificate('/'.join([dir_path, CREDENTIALS_FILE]))
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://missionout.firebaseio.com'})
    return cred


def setup_firebase_gcf_environment():
    if not len(firebase_admin._apps):
        # ensures that app hasn't already been initialized
        firebase_admin.initialize_app()
