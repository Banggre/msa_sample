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
    try:
        data = request.json
        activity_id = ActivityService.add_activity(data)
        return jsonify({"message": "Shelter volunteer event added", "activity_id": str(activity_id)}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Failed to add activity", "error": str(e)}), 500

@auth_bp.route('/get', methods=['GET'])
def get_activity():
    try:
        name = request.args.get('name')
        activity = ActivityService.get_activity(name)
        return jsonify({"message": "Activity found", "activity": activity}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": "Failed to get activity", "error": str(e)}), 500

@auth_bp.route('/add_user_activity_rewards', methods=['POST'])
def add_user_activity_rewards():
    try:
        data = request.json
        ActivityService.add_user_activity_rewards(data["user_id"], data["activity_id"])
        return jsonify({"message": "User activity rewards added"}), 201
    except Exception as e:
        return jsonify({"message": "Failed to add user activity rewards", "error": str(e)}), 500

@auth_bp.route('/get_user_activity_rewards', methods=['GET'])
def get_user_activity_rewards():
    try:
        data = request.json
        rewards_list = ActivityService.get_user_activity_rewards(data["user_id"])
        return jsonify({
            "message": "User activity rewards found", 
            "user_activity_rewards": rewards_list,
        }), 200
    except Exception as e:
        return jsonify({"message": "Failed to get user activity rewards", "error": str(e)}), 500

@auth_bp.route('/update_user_activity_rewards', methods=['POST'])
def update_user_activity_rewards():
    try:
        data = request.json
        ActivityService.update_user_activity_rewards(data["activity_id_list"], data["rewarded"])
        return jsonify({"message": "User activity rewards updated"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to update user activity rewards", "error": str(e)}), 500