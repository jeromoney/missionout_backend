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
    print(event)
    db = firestore.client()
    user_info = {'isEditor': False,
                 'uid': event.get('uid', None),
                 'displayName': event.get('displayName'),
                 'teamID': None}
    db.collection('users').document().set(user_info)



def gcf_entry(event: dict):
    FirebaseSetup.setup_firebase_gcf_environment()
    user_setup(event)


if __name__ == '__main__':
    FirebaseSetup.setup_firebase_local_environment()
    test_event = {'uid':'some uid', 'displayName': 'Joe Blow'}
    user_setup(test_event)
    # setup firestore environment
    # add user
