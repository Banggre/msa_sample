from pymongo import MongoClient
from config import Config

print(Config.MONGO_URI)

client = MongoClient(Config.MONGO_URI)
db = client.reward_db

if "rewards" not in db.list_collection_names():
    db.create_collection("rewards")

rewards_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "point"],
        "properties": {
            "user_id": {
                "bsonType": "string",
                "description": "user_id (required)"
            },
            "point": {
                "bsonType": "number", 
                "description": "point (required)",
            }
        }
    }
}

db.command("collMod", "rewards", validator=rewards_schema)
rewards_collection = db.rewards