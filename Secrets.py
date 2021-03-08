from google.cloud import secretmanager

ACCOUNT_SID_KEY = 'projects/76139268481/secrets/twilio_ACCOUNT_SID/versions/latest'
AUTH_TOKEN_KEY = 'projects/76139268481/secrets/twilio_AUTH_TOKEN/versions/latest'


def twilio_secrets():
    client = secretmanager.SecretManagerServiceClient()

    response = client.access_secret_version(name=ACCOUNT_SID_KEY)
    account_sid = response.payload.data.decode('UTF-8')

    response = client.access_secret_version(name=AUTH_TOKEN_KEY)
    auth_token = response.payload.data.decode('UTF-8')

    return account_sid, auth_token


if __name__ == "__main__":
    import os

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../secrets/secret_manager.json"
    print(twilio_secrets())
