from google.cloud import secretmanager
import json
import cloud_config

secret_keys = [
    "twilio_account_sid",
    "twilio_auth_token",
    "oauth_secret",
    "oauth_token",
    "flask_secret_key",
]


def get_secret_value(key):
    assert key in secret_keys
    client = secretmanager.SecretManagerServiceClient()
    secrets_config = cloud_config.get_config(module="secrets")
    parent = client.secret_version_path(secrets_config.get("project_id"), key, "latest")
    response = client.access_secret_version(name=parent)
    response = response.payload.data.decode("UTF-8")
    assert isinstance(response, str)
    if response[0] == "{":
        response = response.replace("'", '"')
        return json.loads(response)
    else:
        return response


def set_secret_value(key, value):
    assert key in secret_keys
    client = secretmanager.SecretManagerServiceClient()
    secrets_config = cloud_config.get_config(module="secrets")
    parent = client.secret_path(secrets_config.get("project_id"), key)
    if isinstance(value, dict):
        value = str(value)
    payload = value.encode("UTF-8")
    response = client.add_secret_version(
        request={"parent": parent, "payload": {"data": payload}}
    )
    print("Added secret version: {}".format(response.name))
