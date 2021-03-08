"""
Initiates a mission from a watched email account
(0) Dispatch sends email to specific account
(1) Gmail publishes email to topic
(2) Google Cloud Function is triggered by push notification
(3) Function builds a document and saves it to appropriate folder <--- this function below
(4) SendPage function take is from here
"""


def initiate_mission_from_email(event: dict, local_environment=False):
    print(f"my own special code:{event}")


if __name__ == "__main__":
    pass
