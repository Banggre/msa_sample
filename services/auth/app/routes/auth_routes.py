from flask import Blueprint, request, jsonify
from service.auth_service import signup, login
import jwt
import datetime
import os

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup_route():
    user_data = request.json
    user_id, error = signup(user_data)
    
    if error:
        return {"message": error}, 400
    
    return jsonify({"message": "User created", "user_id": str(user_id)}), 201

@auth_bp.route("/login", methods=["GET"])
def login_route():
    data = request.json
    user_id, error = login(data["email"], data["password"])
    
    if error:
        return {"message": error}, 401
    
    return jsonify({"message": "Login successful", "user_id": str(user_id)}), 200