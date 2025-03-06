from models.user_model import users_collection

class UserRepository:
    @staticmethod
    def create_user(user_data):
        return users_collection.insert_one(user_data).inserted_id

    @staticmethod
    def find_user_by_email(email):
        return users_collection.find_one({"email": email})

    @staticmethod
    def find_user_by_email_and_password(email, password):
        return users_collection.find_one({"email": email, "password": password})