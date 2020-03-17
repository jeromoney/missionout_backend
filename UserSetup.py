# Flow: User authenticates on app and triggers an authentication on the backend.
# Outcome: Firestore adds document to users collection with appropriate fields

import FirebaseSetup
from firebase_admin import firestore


def user_setup(event: dict):
    db = firestore.client()
    email = event.get('email', None)
    domain = email.split('@')[1]
    uid = event['uid']
    user_info = {'isEditor': False,
                 'uid': uid,
                 'displayName': event.get('displayName'),
                 'teamID': domain,
                 'email': email}
    db.collection('users').document(uid).set(user_info)


def gcf_entry(event: dict):
    FirebaseSetup.setup_firebase_gcf_environment()
    user_setup(event)


if __name__ == '__main__':
    FirebaseSetup.setup_firebase_local_environment()
    test_event = {'uid': 'some uid', 'displayName': 'Joe Blow'}
    user_setup(test_event)
    # setup firestore environment
    # add user
