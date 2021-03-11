import firebase_admin

import Utils


def setup_firebase_environment():
    if Utils.is_local_environment():
        import os
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/justin/PycharmProjects/secrets/firebase_credentials.json"
        os.environ["FIREBASE_CONFIG"] = "/Users/justin/PycharmProjects/secrets/firebase_credentials.json"
    try:
        app = firebase_admin.initialize_app()
        assert (type(app) is firebase_admin.App)
        return app
    except ValueError:
        print("App is already initialized")


if __name__ == '__main__':
    Utils.set_local_environment()
    print(setup_firebase_environment())
