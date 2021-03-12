from google.cloud import secretmanager
import json
import Utils
import Config

secrets_config = Config.secrets_config()
key_template = secrets_config.get('key_template')


def twilio_secrets():
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=key_template.format(key_name=secrets_config.get('account_sid_key')))
    account_sid = response.payload.data.decode('UTF-8')
    response = client.access_secret_version(name=key_template.format(key_name=secrets_config.get('auth_token_key')))
    auth_token = response.payload.data.decode('UTF-8')
    return account_sid, auth_token


def mission_email():
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=key_template.format(key_name=secrets_config.get('mission_email')))
    return response.payload.data.decode('UTF-8')


def oauth_client_secret():
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=key_template.format(key_name=secrets_config.get('oauth_secret')))
    return json.loads(response.payload.data.decode('UTF-8'))


if __name__ == "__main__":
    Utils.set_local_environment()
    print(twilio_secrets())
    print(mission_email())
    print(oauth_client_secret())
