import firebase_admin


def setup_firebase_environment(local_environment=False):
    if local_environment:
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
    print(setup_firebase_environment(local_environment=True))
