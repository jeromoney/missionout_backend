# Flow: User authenticates on app and triggers an authentication on the backend.
# Outcome: Firestore adds document to users collection with appropriate fields

import FirebaseSetup
from firebase_admin import firestore


def user_setup(event: dict):
    db = firestore.client()
    print(event)
    email = event.get('email', None)
    domain = email.split('@')[1]
    # Check if domain is already a team. If so, automatically assign them to team.
    # If not, assign None which the app will pick up as not on a team
    doc = db.document('teamDomains/domains').get().to_dict()
    if domain in doc['domains']:
        assignedDomain = domain
    else:
        assignedDomain = None

    uid = event['uid']
    user_info = {'isEditor': False,
                 'uid': uid,
                 'displayName': event.get('displayName'),
                 'teamID': assignedDomain,
                 'email': email}
    db.collection('users').document(uid).set(user_info)

if __name__ == '__main__':
    FirebaseSetup.setup_firebase_local_environment()
    test_event = {'uid': 'some uid', 'displayName': 'Joe Blow', 'email': 'joe.blow@chaffeecountysarnorth.org'}
    user_setup(test_event)
