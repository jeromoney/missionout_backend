import sys

sys.path.append("/Users/justin/Projects/missionout_backend")
import unittest


class DocumentWrite2MissionTestCase(unittest.TestCase):
    def test_existing_document_with_bad_data(self):
        import email2mission.documentWrite2mission

        event = {
            "value": {
                "createTime": "2020-02-20T22:08:29.494223Z",
                "fields": {
                    "webhookSource": {"stringValue": "WebhookSender.SENDGRID"},
                },
                "name": 'projects/missionout/databases/("default)/webhook/4daMHXU08fwxlAd6Mp4I',
            },
        }
        result, message = email2mission.documentWrite2mission.documentWrite2mission(
            event
        )
        from google.cloud.firestore_v1.batch import WriteBatch

        self.assertIsInstance(result, WriteBatch)
        self.assertIn("found error while processing webhook", message)

    def test_new_document(self):
        import email2mission.documentWrite2mission

        event = {
            "value": {
                "createTime": "2020-02-20T22:08:29.494223Z",
                "fields": {
                    "webhookSource": {"stringValue": "WebhookSender.SENDGRID"},
                },
                "name": 'projects/missionout/databases/("default)/webhook/fTtAuZHned71K2tvDSly',
            },
        }
        result, message = email2mission.documentWrite2mission.documentWrite2mission(
            event
        )
        from google.cloud.firestore_v1.batch import WriteBatch

        self.assertIsInstance(result, WriteBatch)

    def test_existing_document_with_good_data(self):
        import email2mission.documentWrite2mission

        event = {
            "value": {
                "createTime": "2020-02-20T22:08:29.494223Z",
                "fields": {
                    "webhookSource": {"stringValue": "WebhookSender.SENDGRID"},
                },
                "name": 'projects/missionout/databases/("default)/webhook/DDIKItRYKftVV7Bab2bO',
            },
        }
        result, message = email2mission.documentWrite2mission.documentWrite2mission(
            event
        )
        from google.cloud.firestore_v1.batch import WriteBatch

        self.assertIsInstance(result, WriteBatch)
        self.assertEqual(
            message,
            "Document already exists. This means the message has already been processed.",
        )

    def test_google_document(self):
        import email2mission.documentWrite2mission

        event = {
            "value": {
                "createTime": "2020-02-20T22:08:29.494223Z",
                "fields": {
                    "webhookSource": {"stringValue": "WebhookSender.GOOGLE"},
                },
                "name": 'projects/missionout/databases/("default)/webhook/x6B4FCzgMATDvQKZaNNI',
            },
        }
        result, message = email2mission.documentWrite2mission.documentWrite2mission(
            event
        )
        from google.cloud.firestore_v1.batch import WriteBatch

        self.assertIsInstance(result, WriteBatch)

    def test_sendgrid_document(self):
        import email2mission.documentWrite2mission

        event = {
            "value": {
                "createTime": "2020-02-20T22:08:29.494223Z",
                "fields": {
                    "webhookSource": {"stringValue": "WebhookSender.SENDGRID"},
                },
                "name": 'projects/missionout/databases/("default)/webhook/DDIKItRYKftVV7Bab2bO',
            },
        }
        result, message = email2mission.documentWrite2mission.documentWrite2mission(
            event
        )
        from google.cloud.firestore_v1.batch import WriteBatch

        self.assertIsInstance(result, WriteBatch)


if __name__ == "__main__":
    unittest.main()
