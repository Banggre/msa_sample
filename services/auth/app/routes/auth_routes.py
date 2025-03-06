from flask import Blueprint, request, jsonify
from config import SECRET_KEY 
from repository.user_repository import UserRepository
import jwt
import datetime
import os

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    existing_user = UserRepository.find_user_by_username(data["username"])
    if existing_user:
        return {"message": "username already exists"}, 400
    
    user_id = UserRepository.create_user(data)
    return jsonify({"message": "User created", "user_id": str(user_id)}), 201

@auth_bp.route("/login", methods=["GET"])
def login():
    data = request.json
    user = UserRepository.find_user_by_username_and_password(data["username"], data["password"])
    if not user:
        return {"message": "Invalid username or password"}, 401
    
    token = jwt.encode(
        {"user_id": str(user["_id"]), "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)},
        SECRET_KEY,
        algorithm="HS256",
    )
    return jsonify({"message": "Login successful", "token": token}), 200