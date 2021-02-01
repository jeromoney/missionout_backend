# Flow: User authenticates on app and triggers an authentication on the backend.
# Outcome: Firestore adds document to users collection with appropriate fields

import FirebaseSetup
from firebase_admin import firestore


def user_setup(event: dict):
    db = firestore.client()
    email = event.get('email', None)
    # If a user signs in with a password, they don't need to prove they own their email, which creates a security risk.
    # Instead a DBA will need to manually approve email/password sign ins.
    if 'providerData' in event.keys():
        provider = event['providerData'][0]['providerId']
    else:
        print("Error in event data: " + str(event))
        return
    if provider != 'password':
        domain = email.split('@')[1]
    else:
        domain = None
    # Check if domain is already a team. If so, automatically assign them to team.
    # If not, assign None which the app will pick up as not on a team
    doc = db.document('teamDomains/domains').get().to_dict()
    if domain in doc['domains']:
        assigned_domain = domain
    else:
        assigned_domain = None

    uid = event['uid']
    user_info = {'isEditor': False,
                 'uid': uid,
                 'displayName': event.get('displayName'),
                 'teamID': assigned_domain,
                 'email': email,
                 'dateCreated': firestore.SERVER_TIMESTAMP}
    db.collection('users').document(uid).set(user_info)


if __name__ == '__main__':
    FirebaseSetup.setup_firebase_local_environment()
    test_event = {'providerData': [{'providerId': 'demoteam.com'}], 'uid': 'some uid', 'displayName': 'Joe Blow', 'email': 'joe.blow@chaffeecountysarnorth.org'}
    user_setup(test_event)
