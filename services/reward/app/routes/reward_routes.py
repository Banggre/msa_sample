from flask import Blueprint, request, jsonify
from config import SECRET_KEY
from repository.reward_repository import RewardRepository
import jwt
import datetime
import os
import requests

auth_bp = Blueprint("auth", __name__)

ACTIVITY_SERVICE_URL = "http://activity:8081"

@auth_bp.route('/get_user_activity_history', methods=['GET'])
def get_user_activity_history_within_seven_days():
    try:
        headers = {
            "Authorization": request.headers.get("Authorization"),
            "Content-Type": "application/json"
        }

        response = requests.get(f"{ACTIVITY_SERVICE_URL}/get_user_activity_rewards", headers=headers)

        if response.status_code == 200:
            activities = response.json()
            return jsonify({"success": True, "activities": activities["user_activity_rewards"]}), 200
        else:
            return jsonify({"success": False, "message": "Failed to fetch activities"}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "message": str(e)}), 500
    auth_header = request.headers.get("Authorization") 
    if not auth_header:
        return jsonify({"message": "Authorization header is missing"}), 401


@auth_bp.route('/handle_reward', methods=['POST'])
def handle_reward():
    try:
        # Get user activity rewards
        headers = {
            "Authorization": request.headers.get("Authorization"),
            "Content-Type": "application/json"
        }

        response = requests.get(f"{ACTIVITY_SERVICE_URL}/get_user_activity_rewards", headers=headers)
        
        if response.status_code != 200:
            return jsonify({"success": False, "message": "Failed to fetch activities"}), response.status_code

        activities = response.json()["user_activity_rewards"]
        # Filter unrewarded activities
        unrewarded = [activity for activity in activities if not activity["rewarded"]]
        
        # Separate by type
        volunteering = [activity for activity in unrewarded if activity["activity_type"] == "Volunteering"]
        adoption = [activity for activity in unrewarded if activity["activity_type"] == "Adoption"]
        
        # Calculate points and track used activities
        volunteering_count = len(volunteering) // 3 * 3  # Only count complete sets of 3
        used_volunteering = volunteering[:volunteering_count]
        unused_volunteering = volunteering[volunteering_count:]
        
        volunteering_points = (volunteering_count // 3) * 50  # 50 points per 3 volunteering activities
        adoption_points = len(adoption) * 500  # 500 points per adoption
        total_points = volunteering_points + adoption_points
        
        # Get reward IDs to update (only for activities used in point calculation)
        activity_ids = [activity["activity_id"] for activity in used_volunteering + adoption]
        unused_activity_ids = [activity["activity_id"] for activity in unused_volunteering]
        
        if not activity_ids:
            return jsonify({"success": True, "message": "No new rewards to process"}), 200
            
        # Update activities as rewarded
        update_response = requests.post(
            f"{ACTIVITY_SERVICE_URL}/update_user_activity_rewards",
            headers=headers,
            json={
                "activity_id_list": activity_ids,
                "rewarded": True
            }
        )
        
        if update_response.status_code != 200:
            requests.post(
                f"{ACTIVITY_SERVICE_URL}/update_user_activity_rewards",
                headers=headers,
                json={
                    "activity_id_list": activity_ids,
                    "rewarded": False
                }
            )
            return jsonify({"success": False, "message": "Failed to update rewards status"}), update_response.status_code

        auth_header = request.headers.get("Authorization") 
        if not auth_header:
            return jsonify({"message": "Authorization header is missing"}), 401
        
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded["user_id"]
        try:
            RewardRepository.update_reward_by_user_id(user_id, total_points)
        except Exception as e:
            # Rollback rewards status if points update fails
            requests.post(
                f"{ACTIVITY_SERVICE_URL}/update_user_activity_rewards",
                headers=headers,
                json={"activity_id_list": activity_ids, "rewarded": False}
            )
            return jsonify({"success": False, "message": str(e)}), 500
            
        return jsonify({
            "success": True,
            "message": "Rewards processed successfully",
            "points_earned": total_points,
            "volunteering_count": len(volunteering),
            "adoption_count": len(adoption)
        }), 200
            
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "message": str(e)}), 500