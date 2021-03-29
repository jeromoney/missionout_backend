import os
from flask import abort
from werkzeug.security import check_password_hash
from google.cloud import firestore


def _validate_sendgrid_request(request):
    """Check username and password in webhook request"""
    if request.authorization:
        username = request.authorization.username
        password = request.authorization.password
        return username == os.environ.get("SENDGRID_USERNAME") and check_password_hash(
            os.environ.get("SENDGRID_PASSWORD_HASH"), password
        )
    else:
        return False


def receiveEmailWebhook(request):
    if not _validate_sendgrid_request(request):
        return abort(403)
    # STORE THE EVENT
    item_list = [item for item in request.form.items()]
    item_dict = {item[0]: item[1] for item in item_list}
    item_dict["webhookTimestamp"] = firestore.SERVER_TIMESTAMP
    item_dict["webhookSource"] = "WebhookSender.SENDGRID"
    db = firestore.Client()
    db.collection(u"webhook").document().create(item_dict)
    # PROCESS THE EVENT

    return "Ok", 200
