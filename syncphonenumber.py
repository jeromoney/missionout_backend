"""Temporary sync file is necessary while people have different versions of app"""
from google.cloud import firestore


def deletephonenumber(event: dict):
    db = firestore.Client()
    fields = event["oldValue"]["fields"]
    uid = fields["uid"]["stringValue"]
    del fields["uid"]
    new_fields = {key: list(fields[key].values())[0] for key in fields}
    doc_ref = db.collection("users").document(document_id=uid)
    doc_ref.update({u"phoneNumbers": firestore.ArrayRemove([new_fields])})


def addphonenumber(event: dict):
    db = firestore.Client()
    fields = event["value"]["fields"]
    uid = fields["uid"]["stringValue"]
    del fields["uid"]
    new_fields = {key: list(fields[key].values())[0] for key in fields}
    doc_ref = db.collection("users").document(document_id=uid)
    doc_ref.update({u"phoneNumbers": firestore.ArrayUnion([new_fields])})