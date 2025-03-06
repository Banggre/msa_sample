from repository.reward_repository import RewardRepository
import requests

class RewardService:
    ACTIVITY_SERVICE_URL = "http://activity:8081"

    @staticmethod
    def process_user_rewards(user_id):
        # Get user activity rewards
        response = requests.get(
            f"{RewardService.ACTIVITY_SERVICE_URL}/get_user_activity_rewards", 
            json={"user_id": user_id}
        )
        
        if response.status_code != 200:
            raise Exception("Failed to fetch activities")

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
        
        # Get reward IDs to update
        activity_ids = [activity["activity_id"] for activity in used_volunteering + adoption]
        
        if not activity_ids:
            return {
                "points_earned": 0,
                "volunteering_count": len(volunteering),
                "adoption_count": len(adoption)
            }
            
        # Update activities as rewarded
        RewardService._update_activity_rewards(activity_ids, True)
        
        try:
            RewardRepository.update_reward_by_user_id(user_id, total_points)
        except Exception as e:
            # Rollback rewards status if points update fails
            RewardService._update_activity_rewards(activity_ids, False)
            raise Exception(f"Failed to update points: {str(e)}")
            
        return {
            "points_earned": total_points,
            "volunteering_count": len(volunteering),
            "adoption_count": len(adoption)
        }

    @staticmethod
    def _update_activity_rewards(activity_ids, rewarded):
        response = requests.post(
            f"{RewardService.ACTIVITY_SERVICE_URL}/update_user_activity_rewards",
            json={
                "activity_id_list": activity_ids,
                "rewarded": rewarded
            }
        )
        
        if response.status_code != 200:
            raise Exception("Failed to update rewards status")
