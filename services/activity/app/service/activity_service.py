from repository.activity_repository import ActivityRepository
from repository.user_activity_rewards_repository import UserActivityRewardsRepository

class ActivityService:
    @staticmethod
    def add_activity(data):
        existing_activity = ActivityRepository.find_activity_by_name(data["name"])
        if existing_activity:
            raise ValueError("Activity already exists")
        return ActivityRepository.create_activity(data)

    @staticmethod
    def get_activity(name):
        activity = ActivityRepository.find_activity_by_name(name)
        if not activity:
            raise ValueError("Activity not found")
        return {
            "id": str(activity["_id"]),
            "name": activity["name"],
            "type": activity["type"]
        }

    @staticmethod
    def add_user_activity_rewards(user_id, activity_id):
        return UserActivityRewardsRepository.create_user_activity_rewards(user_id, activity_id)

    @staticmethod
    def get_user_activity_rewards(user_id):
        user_activity_rewards = UserActivityRewardsRepository.find_user_activity_rewards_within_seven_days(user_id)
        rewards_list = []
        for reward in user_activity_rewards:
            rewards_list.append({
                "id": str(reward["_id"]),
                "activity_id": reward["activity_id"],
                "created_at": reward["created_at"],
                "rewarded": reward["rewarded"]
            })
        # activity_ids = []
        # for reward in rewards_list:
        #     activity_ids.append(reward["activity_id"])
        # activity_ids = list(set(activity_ids))
        # activities = ActivityRepository.find_activity_by_ids(activity_ids)
        # activities_dict = {str(activity["_id"]): activity for activity in list(activities)}
        # for reward in rewards_list:
        #     reward["activity_name"] = activities_dict[reward["activity_id"]]["name"]
        #     reward["activity_type"] = activities_dict[reward["activity_id"]]["type"]
        
        activity_ids = list(set(reward["activity_id"] for reward in rewards_list))
        activities = ActivityRepository.find_activity_by_ids(activity_ids)
        activities_dict = {str(activity["_id"]): activity for activity in list(activities)}
        
        for reward in rewards_list:
            reward["activity_name"] = activities_dict[reward["activity_id"]]["name"]
            reward["activity_type"] = activities_dict[reward["activity_id"]]["type"]
        
        return rewards_list

    @staticmethod
    def update_user_activity_rewards(activity_id_list, rewarded):
        return UserActivityRewardsRepository.update_user_activity_rewards(activity_id_list, rewarded)
