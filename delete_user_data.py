# When a user is deleted in FirebaseAuth, associated data in firestore is also deleted.

# Flow: User authenticates on app and triggers an authentication on the backend.
# Outcome: Firestore deletes user's data

import firebase_setup
from firebase_admin import firestore


def delete_user_data(event: dict):
    db = firestore.client()
    uid = event.get('uid', None)
    db.collection('users').document(uid).delete()


if __name__ == '__main__':
    import utils
    utils.set_local_environment()
    firebase_setup.setup_firebase_environment()
    test_event = {"email": "me@example.com",
                  "metadata": {
                      "createdAt": "2018-10-19T19:29:16Z"
                  },
                  "uid": "01iAD7ZRJdahYePK529zVhkRj8p1"
                  }
    delete_user_data(test_event)
