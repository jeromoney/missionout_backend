from google.cloud import secretmanager

PROJECT_ID = 'missionout'
VERSION_ID = 1
ACCOUNT_SID_KEY = 'twilio_ACCOUNT_SID'
AUTH_TOKEN_KEY = 'twilio_AUTH_TOKEN'


def twilio_secrets():
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path(PROJECT_ID, ACCOUNT_SID_KEY, VERSION_ID)
    response = client.access_secret_version(name)
    account_sid = response.payload.data.decode('UTF-8')

    name = client.secret_version_path(PROJECT_ID, AUTH_TOKEN_KEY, VERSION_ID)
    response = client.access_secret_version(name)
    auth_token = response.payload.data.decode('UTF-8')

    return account_sid, auth_token
