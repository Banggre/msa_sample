from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.volunteer_db

if "users" not in db.list_collection_names():
    db.create_collection("users")

user_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["email", "password"],
        "properties": {
            "email": {
                "bsonType": "string",
                "description": "user email (required)"
            },
            "password": {
                "bsonType": "string",
                "description": "password (required)"
            }
        }
    }
}

db.command("collMod", "users", validator=user_schema)
users_collection = db.users