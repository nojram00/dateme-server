from server.db import create_connection

class Profile:
    def __init__(self):
        self.collection = create_connection()['profiles']

    def get_profiles(self):
        results = self.collection.find()
        profiles = []
        for result in results:
            result['_id'] = str(result['_id'])
            profiles.append(result)
        return profiles