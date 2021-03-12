from google.cloud import secretmanager
import json
import Utils
import Config

secrets_config = Config.secrets_config()


def _get_secret_value(key: str):
    client = secretmanager.SecretManagerServiceClient()
    parent = client.secret_version_path(secrets_config.get('project_id'), key, 'latest')
    response = client.access_secret_version(name=parent)
    return response.payload.data.decode('UTF-8')


def get_twilio_secrets():
    account_sid_key = secrets_config.get('account_sid_key')
    auth_token_key = secrets_config.get('auth_token_key')
    return _get_secret_value(account_sid_key), _get_secret_value(auth_token_key)


def get_mission_email():
    mission_email = secrets_config.get('mission_email')
    return _get_secret_value(mission_email)


def get_oauth_client_secret():
    oauth_secret = secrets_config.get('oauth_secret')
    return json.loads(_get_secret_value(oauth_secret))


def get_oauth_token():
    oauth_token = secrets_config.get('oauth_token')
    return json.loads(_get_secret_value(oauth_token))


def _set_secret_value(key: str, value: str):
    client = secretmanager.SecretManagerServiceClient()
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
    print(get_twilio_secrets())
    print(get_mission_email())
    print(get_oauth_client_secret())
    print(get_oauth_token())
