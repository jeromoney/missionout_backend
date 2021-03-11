import os

TEST_RESOURCE_STR = '{\"oldValue\": {}, \"updateMask\": {}, \"value\": {\"createTime\": ' \
                    '\"2020-02-20T22:08:29.494223Z\", ' \
                    '\"fields\": {\"needForAction\": {\"stringValue\": \"we need kisses for the puppy\"}, ' \
                    '\"missionDocumentPath\": {' \
                    '\"stringValue\": \"/teams/demoteam.com/missions/wIdTaPhiEOB4VZmEd2e6\"}, \"creator\": {' \
                    '\"stringValue\": \"Justin Matis\"}, ' \
                    '\"description\": {\"stringValue\": \"A puppy got hurt\"}, \"time\": {\"timestampValue\": ' \
                    '\"2020-02-20T22:08:29.415Z\"}, \"onlyEditors\": {\"booleanValue\": ' \
                    'true}}, \"name\": \"projects/missionout/databases/(' \
                    'default)/documents/teams/demoteam.com/missions/wLZ6aZy6pVRBJBCkZXeu/pages' \
                    '/icGulF5jyDuqBMnyuD2I\", \"updateTime\": \"2020-02-20T22:08:29.494223Z\"}}'


def get_teamID_from_event(event):
    """Event is JSON values passed by Google Cloud Function. We dig through data to get the ID of the team"""
    teamIDPath = event['value']['name'].split('/')
    for i, word in enumerate(teamIDPath):
        if word == 'teams':
            return teamIDPath[i + 1]
    else:  # if value is not found, this code is called
        raise ValueError('expected to find teamID in path')


def is_local_environment():
    result = os.getenv("LOCAL_ENVIRONMENT", default=False)
    return result == 'True'


def set_local_environment():
    os.environ["LOCAL_ENVIRONMENT"] = 'True'
    assert is_local_environment()


if __name__ == "__main__":
    import json

    test_event = json.loads(TEST_RESOURCE_STR)
    print(get_teamID_from_event(test_event))
