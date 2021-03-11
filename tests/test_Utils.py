import unittest
import json
from Utils import get_teamID_from_event, TEST_RESOURCE_STR

ERROR_RESOURCE_STR = '{\"oldValue\": {}, \"updateMask\": {}, \"value\": {\"createTime\": \"2020-02-20T22:08:29.494223Z\", ' \
                        '\"fields\": {\"needForAction\": {\"stringValue\": \"we need kisses for the puppy\"}, \"address\": {' \
                        '\"stringValue\": \"wLZ6aZy6pVRBJBCkZXeu\"}, \"creator\": {\"stringValue\": \"Justin Matis\"}, ' \
                        '\"description\": {\"stringValue\": \"A puppy got hurt\"}, \"time\": {\"timestampValue\": ' \
                        '\"2020-02-20T22:08:29.415Z\"}}, \"name\": \"projects/missionout/databases/(' \
                        'default)/documents/kilgore/chaffeecountysarnorth.org/missions/wLZ6aZy6pVRBJBCkZXeu/pages' \
                        '/icGulF5jyDuqBMnyuD2I\", \"updateTime\": \"2020-02-20T22:08:29.494223Z\"}}'


class UtilsTest(unittest.TestCase):
    def test_get_teamID_from_event(self):
        test_event = json.loads(TEST_RESOURCE_STR)
        teamID = get_teamID_from_event(test_event)
        self.assertTrue(teamID == 'chaffeecountysarnorth.org')

        test_event = json.loads(ERROR_RESOURCE_STR)
        #teamID = get_teamID_from_event(test_event) -- Raises an exception which is the expected behavior


if __name__ == '__main__':
    unittest.main()