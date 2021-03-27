from google.cloud import firestore


def process_emails(message_dict: dict):
    db = firestore.Client()
    foo = firestore.SERVER_TIMESTAMP
    batch = db.batch()
    for message_key in message_dict:
        indvidual_dict = message_dict[message_key]
        indvidual_dict["webhookTimestamp"] = firestore.SERVER_TIMESTAMP
        indvidual_dict["webhookSource"] = "WebhookSender.GOOGLE"
        message_ref = db.collection("webhook").document()
        batch.set(message_ref, indvidual_dict)
    # Commit the batch
    batch.commit()
