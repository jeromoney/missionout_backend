import sys

sys.path.append("/Users/justin/Projects/missionout_backend")
import pytest
import unittest
from email2mission.documentWrite2mission import documentWrite2mission
from google.cloud.firestore_v1.batch import WriteBatch


class ContestMock:
    def __init__(self, document_id: str):
        self.resource = (
            f"projects/missionout/databases/(default)/documents/webhook/{document_id}"
        )


class DocumentWrite2MissionTestCase(unittest.TestCase):
    def test_existing_document_with_bad_data(self):
        context = ContestMock(document_id="2ytOUdOkNXz6QrdPHfdU")
        result, message = documentWrite2mission({}, context)
        self.assertIsInstance(result, WriteBatch)
        self.assertIn("found error while processing webhook", message)

    def test_existing_document_with_good_data(self):
        context = ContestMock(document_id="Y5DYTcgvt2GnXKCwhDyb")
        result, message = documentWrite2mission({}, context)
        self.assertIsInstance(result, WriteBatch)
        self.assertEqual(
            message,
            "Document already exists. This means the message has already been processed.",
        )

    def test_google_document_with_wrong_mimetype(self):
        context = ContestMock(document_id="NRtObX1uR62oP3jejZ92")
        result, message = documentWrite2mission({}, context)
        self.assertIsInstance(result, WriteBatch)
        self.assertIn("Only plain text messages are accepted", message)

    def test_google_document_with_correct_mimetype(self):
        context = ContestMock(document_id="fR52hY8FAo7IbJc01Wye")
        result, message = documentWrite2mission({}, context)
        self.assertIsInstance(result, WriteBatch)
        self.assertEqual("success", message)

    def test_sendgrid_document(self):
        context = ContestMock(document_id="Y5DYTcgvt2GnXKCwhDyb")
        result, message = documentWrite2mission({}, context)
        self.assertIsInstance(result, WriteBatch)

    def test_no_matching_document(self):
        context = ContestMock(document_id="some wrong id")
        with pytest.raises(FileNotFoundError):
            documentWrite2mission({}, context)


if __name__ == "__main__":
    unittest.main()
