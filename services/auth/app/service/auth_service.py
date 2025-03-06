from repository.user_repository import UserRepository
import datetime

def signup(user_data):
    existing_user = UserRepository.find_user_by_email(user_data["email"])
    if existing_user:
        return None, "email already exists"
    
    user_id = UserRepository.create_user(user_data)
    return user_id, None

def login(email, password):
    user = UserRepository.find_user_by_email_and_password(email, password)
    if not user:
        return Nonde, "Invalid email or password"

    return user["_id"], None