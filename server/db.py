import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    client = MongoClient(os.getenv('MONGO_DB_URL'))
    db = client['dateme']
    return db

if __name__ == "__main__":
    db = create_connection()
    # print(db.list_collection_names())
    profiles = db['users']
    print(list([profile for profile in profiles.find()]))