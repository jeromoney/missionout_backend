import base64
import hashlib
from datetime import date
import abc
from abc import ABC, abstractmethod


REQUIRED_KEYS = {"CALL", "PLACE", "ADDR", "CITY", "INFO"}


class Parser(ABC):
    @abstractmethod
    def get_parsed_email(self):
        pass


def parse_email(email: str):
    """Converts email body of value pairs into dictionary

    Args:
        email (str): email body in the Cadpage format
    """
    result = email.splitlines()
    result = [line for line in result if ":" in line]
    result = [line.split(":") for line in result]
    # the fanciness with the join is in case the message has colons in it
    result = {line[0].strip(): ":".join(line[1:]).strip() for line in result}
    # make sure the required keys exist so the format is correct
    if not REQUIRED_KEYS.issubset(result.keys()):
        raise ValueError(
            f"Email is missing essential fields. found {result.keys()} expecting {REQUIRED_KEYS}"
        )

    return result


class ParsedEmail:
    def __init__(*, self, teamId: str, documentId: str, data_dict: dict):
        this.teamId = teamId
        this.documentId = documentId
        this.data_dict = data_dict


class Parserxyz:
    def __init__(
        self,
        request,
        sender_parser,
        body_parser,
        team_parsing_function,
        text_parser=parse_email,
    ):
        this.request = request
        this._sender_parser = sender_parser
        this._body_parser = body_parser
        this._text_parser = text_parser
        this._team_parsing_function = team_parsing_function

    def get_sender(self):
        return this._sender_parser(this.request)

    def get_teamID(self):
        return this._team_parsing_function(this.request)

    def get_body_dict(self):
        return this.text_parser(this.body_parser(this.request))


def _google_parsing_function(request: dict):
    mimeType = request["payload"]["mimeType"]
    if mimeType != "text/plain":
        raise ValueError(f"Only plain text messages are accepted. Found: {mimeType}")
    body_base64 = request["payload"]["body"]["data"]
    # This was an annoying bug to fix. Emojis broke the system when I was just using b64encode
    return base64.urlsafe_b64decode(body_base64).decode("UTF-8")


def _sendgrid_parsing_function(request: dict):
    return request["text"]


def _google_sender_parsing_function(document_dict: dict):
    headers = document_dict["payload"]["headers"]
    for header in headers:
        if header["name"] == "From":
            return header["value"]
    raise ValueError("Could not find sender of email")


def _sendgrid_sender_parsing_function(document_dict: dict):
    return document_dict["from"]


def _get_team_id_from_email(to_address: str):
    """looks up email address and returns the team that it belongs to"""
    db = firestore.Client()
    docs = [
        doc
        for doc in db.collection(get_config("firestore_document_paths")["team_path"])
        .where("missionEmail", "array_contains", to_address)
        .stream()
    ]
    if len(docs) == 0:
        raise ValueError("Could not identify team from message")
    elif len(docs) > 1:
        raise ValueError("More than one team had the same email address")
    else:
        return docs[0].to_dict()["teamID"]


def _google_team_parsing_function(document_dict: dict):
    headers = document_dict["payload"]["headers"]
    for header in headers:
        if header["name"] in ("To", "Cc"):
            to_address = header["value"]
            if "," in to_address:
                to_address = to_address.split(",")[0].strip()
            return _get_team_id_from_email(to_address)

    raise ValueError("Could not find TO/CC header in email")


def _sendgrid_team_parsing_function(document_dict: dict):
    to_address = document_dict["to"].split(",")[0].strip()
    return _get_team_id_from_email(to_address)


def _hasher():
    return hashlib.md5(
        (f"{this.mission_dict}{date.today()}").encode("utf8")
    ).hexdigest()
