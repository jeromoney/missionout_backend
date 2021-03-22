# When a user is deleted in FirebaseAuth, associated data in firestore is also deleted.

# Flow: User authenticates on app and triggers an authentication on the backend.
# Outcome: Firestore deletes user's data

from google.cloud import firestore


def delete_user_data(event: dict):
    db = firestore.Client()
    uid = event.get("uid", None)
    db.collection("users").document(uid).delete()


if __name__ == "__main__":
    test_event = {
        "email": "me@example.com",
        "metadata": {"createdAt": "2018-10-19T19:29:16Z"},
        "uid": "01iAD7ZRJdahYePK529zVhkRj8p1",
    }
    delete_user_data(test_event)
