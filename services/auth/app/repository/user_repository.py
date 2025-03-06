from models.user_model import users_collection

class UserRepository:
    @staticmethod
    def create_user(user_data):
        return users_collection.insert_one(user_data).inserted_id

    @staticmethod
    def find_user_by_username(username):
        return users_collection.find_one({"username": username})

    @staticmethod
    def find_user_by_username_and_password(username, password):
        return users_collection.find_one({"username": username, "password": password})