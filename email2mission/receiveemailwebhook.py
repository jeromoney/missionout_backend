import os
import flask
import requests
import google.oauth2.credentials
from google_auth_oauthlib.flow import Flow
import sys
from flask import abort, Flask, request
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum, unique, auto
from google.cloud import firestore


class WebhookSender(Enum):
    TWILIO = auto()
    GOOGLE = auto()
    SENDGRID = auto()


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


def _validate_request(f):
    """Validates requests from all incoming sources"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        valididation_functions = [
            (_validate_sendgrid_request, WebhookSender.SENDGRID),
        ]
        # Only one validator should pass. Returns enum if valid else returns None
        validation_status = [
            validator[1] if validator[0](request) else None
            for validator in valididation_functions
        ]
        # A list of enum that have passed the test. Should only be one
        validation_results = [
            result for result in validation_status if result is not None
        ]
        if len(validation_results) > 1:
            raise ValueError("More than one validator passed. This is my error")
        elif len(validation_results) == 1:
            return f(*args, **kwargs, validator=validation_results[0])
        else:
            return abort(403)

    return decorated_function


@_validate_request
def receiveEmailWebhook(request, validator: WebhookSender):
    print(request.form)
    # STORE THE EVENT
    webhookTimestamp = firestore.SERVER_TIMESTAMP
    item_list = [item for item in request.form.items()]
    item_dict = {item[0]: item[1] for item in item_list}
    item_dict["webhookTimestamp"] = firestore.SERVER_TIMESTAMP
    item_dict["webhookSource"] = str(validator)
    db = firestore.Client()
    db.collection(u"webhook").document().create(item_dict)
    # PROCESS THE EVENT

    return "Ok", 200