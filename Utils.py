def get_teamID_from_event(event):
    """Event is JSON values passed by Google Cloud Function. We dig through data to get the ID of the team"""
    teamIDPath = event['value']['name'].split('/')
    for i, word in enumerate(teamIDPath):
        if word == 'teams':
            return teamIDPath[i + 1]
    else: # if value is not found, this code is called
        raise ValueError('expected to find teamID in path')