import firebase_admin


def setup_firebase_environment():
    if not firebase_admin._apps:
        app = firebase_admin.initialize_app()
        assert type(app) is firebase_admin.App
        return app
    else:
        return firebase_admin.get_app()


if __name__ == "__main__":
    print(setup_firebase_environment())
