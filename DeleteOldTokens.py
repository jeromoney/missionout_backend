from firebase_admin.auth import ExpiredIdTokenError,InvalidIdTokenError

import FirebaseSetup

from firebase_admin import firestore, auth

def delete_old_tokens():
    db = firestore.client()
    token_refs = db.collection_group('tokens').stream()
    for doc in token_refs:
        token = doc.to_dict().get('token',None)
        try:
            decoded_token = auth.verify_id_token(token, check_revoked=True)
            uid = decoded_token['uid']
            print(uid)
        except (ExpiredIdTokenError,InvalidIdTokenError):
            # delete expired token
            print('Found expired or invalid token')
            db.document(doc.reference.path).delete()




if __name__ == '__main__':
    FirebaseSetup.setup_firebase_local_environment()
    delete_old_tokens()