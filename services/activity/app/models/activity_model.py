from pymongo import MongoClient
from config import Config

print(Config.MONGO_URI)

client = MongoClient(Config.MONGO_URI)
db = client.activity_db

if "activity" not in db.list_collection_names():
    db.create_collection("activity")

activity_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "type"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "activity name (required)"
            },
            "type": {
                "bsonType": "string",
                "enum": ["Volunteering", "Adoption"],
                "description": "activity type volunteering/adoption(required)"
            },
        }
    }
}

db.command("collMod", "activity", validator=activity_schema )
activity_collection = db.activity