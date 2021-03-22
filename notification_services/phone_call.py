from urllib import parse
from twilio.rest import Client

from data import MyMessage, Team
from cloud_secrets import get_secret_value
import cloud_config

twilio_config = cloud_config.twilio_config()


def make_phone_call(event: dict, team: Team):
    account_sid = get_secret_value("twilio_account_sid")
    auth_token = get_secret_value("twilio_auth_token")
    voice_phone_numbers = team.get_voice_phone_numbers()
    message = MyMessage(event)
    need_for_action = parse.quote(message.needForAction)
    description = parse.quote(message.description)
    client = Client(account_sid, auth_token)
    result = {}
    for number in voice_phone_numbers:
        call = client.calls.create(
            # URL is for static announcement
            url=twilio_config.get("call_script_url").format(
                description, need_for_action
            ),
            to=number,
            from_=twilio_config.get("purchased_phone_number"),
        )
        status_str = str(call.status)
        if status_str not in result.keys():
            result[status_str] = 1
        else:
            result[status_str] += 1
    return f"Phone call result: {result}"
