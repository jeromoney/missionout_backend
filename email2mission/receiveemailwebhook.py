def receiveEmailWebhook(event: dict):
    print(event)
    return str(event["data"]), 200
