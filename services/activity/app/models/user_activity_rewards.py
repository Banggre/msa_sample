from pymongo import MongoClient
from config import Config

print(Config.MONGO_URI)

client = MongoClient(Config.MONGO_URI)
db = client.activity_db

if "user_activity_rewards" not in db.list_collection_names():
    db.create_collection("user_activity_rewards")

user_activity_rewards_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "activity_id"],
        "properties": {
            "user_id": {
                "bsonType": "string",
                "description": "user_id (required)"
            },
            "activity_id": {
                "bsonType": "string",
                "description": "activity_id (required)"
            },
            "rewarded": {
                "bsonType": "bool",
                "description": "rewarded",
            },
            "created_at": {
                "bsonType": "date",
                "description": "created date"
            }
        }
    }
}

db.command("collMod", "user_activity_rewards", validator=user_activity_rewards_schema)
user_activity_rewards_collection = db.user_activity_rewards