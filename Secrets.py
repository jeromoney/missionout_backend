from google.cloud import secretmanager

ACCOUNT_SID_KEY = 'projects/76139268481/secrets/twilio_ACCOUNT_SID/versions/latest'
AUTH_TOKEN_KEY = 'projects/76139268481/secrets/twilio_AUTH_TOKEN/versions/latest'
MISSION_EMAIL = 'projects/76139268481/secrets/MISSION_EMAIL/versions/latest'


def set_environment_variables():
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    secret_manager_json = '/'.join([dir_path, "../secrets/secret_manager_credentials.json"])
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = secret_manager_json


def twilio_secrets(local_environment=False):
    if local_environment:
        set_environment_variables()
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=ACCOUNT_SID_KEY)
    account_sid = response.payload.data.decode('UTF-8')
    response = client.access_secret_version(name=AUTH_TOKEN_KEY)
    auth_token = response.payload.data.decode('UTF-8')

    return account_sid, auth_token


def mission_email(local_environment=False):
    if local_environment:
        set_environment_variables()
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=MISSION_EMAIL)
    return response.payload.data.decode('UTF-8')


if __name__ == "__main__":
    set_environment_variables()
    print(twilio_secrets())
    print(mission_email())
