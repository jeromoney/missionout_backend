import yaml
import os

config_file = '/'.join([os.path.dirname(__file__), 'config.yaml'])
config = yaml.safe_load(open(config_file))


def secrets_config():
    return config.get('secrets')


def twilio_config():
    return config.get('twilio')


def email_2_mission_config():
    return config.get('email_2_mission')


if __name__ == '__main__':
    print(secrets_config())
    print(twilio_config())
    print(email_2_mission_config())
