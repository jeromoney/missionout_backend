from google.cloud import secretmanager

import Utils

KEY_TEMPLATE = 'projects/76139268481/secrets/{key_name}/versions/latest'
ACCOUNT_SID_KEY = 'twilio_ACCOUNT_SID'
AUTH_TOKEN_KEY = 'twilio_AUTH_TOKEN'
MISSION_EMAIL = 'MISSION_EMAIL'
OAUTH_SECRET = 'email2missionOauth_client_secret'


def set_environment_variables():
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    secret_manager_json = '/'.join([dir_path, "../secrets/secret_manager_credentials.json"])
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = secret_manager_json


def twilio_secrets():
    if Utils.is_local_environment():
        set_environment_variables()
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=KEY_TEMPLATE.format(key_name=ACCOUNT_SID_KEY))
    account_sid = response.payload.data.decode('UTF-8')
    response = client.access_secret_version(name=KEY_TEMPLATE.format(key_name=AUTH_TOKEN_KEY))
    auth_token = response.payload.data.decode('UTF-8')

    return account_sid, auth_token


def mission_email():
    if Utils.is_local_environment():
        set_environment_variables()
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=KEY_TEMPLATE.format(key_name=MISSION_EMAIL))
    return response.payload.data.decode('UTF-8')


def oauth_client_secret():
    if Utils.is_local_environment():
        set_environment_variables()
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=KEY_TEMPLATE.format(key_name=OAUTH_SECRET))
    return response.payload.data.decode('UTF-8')


if __name__ == "__main__":
    Utils.set_local_environment()
    set_environment_variables()
    print(twilio_secrets())
    print(mission_email())
    print(oauth_client_secret())
