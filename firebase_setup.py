import firebase_admin

import utils


def setup_firebase_environment():
    if utils.is_local_environment():
        import os
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/justin/Projects/secrets/firebase_credentials.json"
        os.environ["FIREBASE_CONFIG"] = "/Users/justin/Projects/secrets/firebase_credentials.json"
    try:
        app = firebase_admin.initialize_app()
        assert (type(app) is firebase_admin.App)
        return app
    except ValueError as e:
        print(f"App is already initialized {e}")


if __name__ == '__main__':
    utils.set_local_environment()
    print(setup_firebase_environment())
