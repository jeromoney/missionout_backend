# Flow: User authenticates on app and triggers an authentication on the backend.
# Outcome: Firestore adds document to users collection with appropriate fields
#
# bool isEditor;
#   String teamID;
#
# voicePhoneNumber;
#
# mobilePhoneNumber;
#
# region;
#
# chatURI;
#
# displayName;
# email;
#
# uid;

import FirebaseSetup
from firebase_admin import firestore


def user_setup(event: dict):
    db = firestore.client()


def gcf_entry(event: dict,
              context):  # context is type of google.cloud.functions.Context but not using variable at moment
    FirebaseSetup.setup_firebase_gcf_environment()
    user_setup(event)


if __name__ == '__main__':
    FirebaseSetup.setup_firebase_local_environment()
    user_setup(None)
    # setup firestore environment
    # add user
