from flask import Request


def receiveEmailWebhook(request: Request):
    print(request)
    return str(request), 200
