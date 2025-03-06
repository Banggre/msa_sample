from flask import Blueprint, request, jsonify
from config import SECRET_KEY
from repository.activity_repository import ActivityRepository
from repository.user_activity_rewards_repository import UserActivityRewardsRepository
import jwt
import datetime
import os

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/add', methods=['POST'])
def add_activity():
    data = request.json
    existing_activity = ActivityRepository.find_activity_by_name(data["name"])
    if existing_activity:
        return jsonify({"message": "Activity already exists"}), 400
    try:
        activity_id = ActivityRepository.create_activity(data)
        return jsonify({"message": "Shelter volunteer event added", "activity_id": str(activity_id)}), 201
    except Exception as e:
        return jsonify({"message": "Failed to add activity", "error": str(e)}), 500

@auth_bp.route('/get', methods=['GET'])
def get_activity():
    name = request.args.get('name')
    activity = ActivityRepository.find_activity_by_name(name)
    if not activity:
        return jsonify({"message": "Activity not found"}), 404
    return jsonify({"message": "Activity found", "activity": {
        "id": str(activity["_id"]),
        "name": activity["name"],
        "type": activity["type"]
    }}), 200

@auth_bp.route('/add_user_activity_rewards', methods=['POST'])
def add_user_activity_rewards():
    auth_header = request.headers.get("Authorization") 
    if not auth_header:
        return jsonify({"message": "Authorization header is missing"}), 401
    
    token = auth_header.split(" ")[1]
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = decoded["user_id"]
    data = request.json
    UserActivityRewardsRepository.create_user_activity_rewards(user_id, data["activity_id"])
    return jsonify({"message": "User activity rewards added"}), 201

@auth_bp.route('/get_user_activity_rewards', methods=['GET'])
def get_user_activity_rewards():
    auth_header = request.headers.get("Authorization") 
    if not auth_header:
        return jsonify({"message": "Authorization header is missing"}), 401
    
    token = auth_header.split(" ")[1]
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = decoded["user_id"]
    try:
        user_activity_rewards = UserActivityRewardsRepository.find_user_activity_rewards_within_seven_days(user_id)
        rewards_list = []
        for reward in user_activity_rewards:
            rewards_list.append({
                "id": str(reward["_id"]),
                "user_id": user_id,
                "activity_id": reward["activity_id"],
                "created_at": reward["created_at"],
                "rewarded": reward["rewarded"]
            })
        activity_ids = []
        for reward in rewards_list:
            activity_ids.append(reward["activity_id"])
        activity_ids = list(set(activity_ids))
        activities = ActivityRepository.find_activity_by_ids(activity_ids)
        activities_dict = {str(activity["_id"]): activity for activity in list(activities)}
        for reward in rewards_list:
            reward["activity_name"] = activities_dict[reward["activity_id"]]["name"]
            reward["activity_type"] = activities_dict[reward["activity_id"]]["type"]
    except Exception as e:
        return jsonify({"message": "Failed to get user activity rewards", "error": str(e)}), 500

    return jsonify({
        "message": "User activity rewards found", 
        "user_activity_rewards": rewards_list,
        "user_id": user_id,
    }), 200

@auth_bp.route('/update_user_activity_rewards', methods=['POST'])
def update_user_activity_rewards():
    data = request.json
    activity_id_list = data["activity_id_list"]
    rewarded = data["rewarded"]
    try:
        UserActivityRewardsRepository.update_user_activity_rewards(activity_id_list, rewarded)
        return jsonify({"message": "User activity rewards updated"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to update user activity rewards", "error": str(e)}), 500