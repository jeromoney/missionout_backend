from google.cloud import secretmanager
import json
import Utils
import Config

secret_keys = [
    'twilio_account_sid',
    'twilio_auth_token',
    'mission_email',
    'oauth_secret',
    'oauth_token',
    'oauth_state'
]


def get_secret_value(key):
    assert key in secret_keys
    client = secretmanager.SecretManagerServiceClient()
    secrets_config = Config.secrets_config()
    parent = client.secret_version_path(secrets_config.get('project_id'), key, 'latest')
    response = client.access_secret_version(name=parent)
    response = response.payload.data.decode('UTF-8')
    if response[0] == '{':
        return json.loads(response)
    else:
        return response


def _set_secret_value(key: str, value: str):
    client = secretmanager.SecretManagerServiceClient()
    secrets_config = Config.secrets_config()
    parent = client.secret_path(secrets_config.get('project_id'), key)
    payload = value.encode("UTF-8")
    response = client.add_secret_version(
        request={"parent": parent, "payload": {"data": payload}}
    )
    print("Added secret version: {}".format(response.name))


def set_oauth_token(oauth_token):
    _set_secret_value(key='oauth_token', value=oauth_token)


def set_oauth_state(oauth_state):
    _set_secret_value(key='oauth_state', value=oauth_state)


if __name__ == "__main__":
    Utils.set_local_environment()
    for key in secret_keys:
        print(get_secret_value(key))
