from pymongo import MongoClient
from config import Config

print(Config.MONGO_URI)

client = MongoClient(Config.MONGO_URI)
db = client.activity_db

if "activities" not in db.list_collection_names():
    db.create_collection("activities")

activities_schema = {
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

db.command("collMod", "activities", validator=activities_schema )
activities_collection = db.activities