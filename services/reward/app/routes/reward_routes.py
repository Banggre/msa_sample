from flask import Blueprint, request, jsonify
from config import SECRET_KEY
from repository.reward_repository import RewardRepository
import jwt
import datetime
import os
import requests

auth_bp = Blueprint("auth", __name__)

ACTIVITY_SERVICE_URL = "http://activity:8081"

@auth_bp.route('/handle_reward', methods=['POST'])
def handle_reward():
    try:
        data = request.json
        user_id = data["user_id"]
        
        result = RewardService.process_user_rewards(user_id)
        
        return jsonify({
            "success": True,
            "message": "Rewards processed successfully",
            **result
        }), 200
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500