from models.user_activity_rewards import user_activity_rewards_collection
from datetime import datetime, timedelta

class UserActivityRewardsRepository:
    @staticmethod
    def create_user_activity_rewards(user_id, activity_id):
        """사용자 추가"""
        return user_activity_rewards_collection.insert_one({
            "user_id": user_id, 
            "activity_id": activity_id,
            "rewarded": False,
            "created_at": datetime.utcnow(),
        }).inserted_id

    @staticmethod
    def find_user_activity_rewards_within_seven_days(user_id):
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        return user_activity_rewards_collection.find({
            "user_id": user_id,
            "created_at": {"$gte": seven_days_ago}
        })
    
    @staticmethod
    def update_user_activity_rewards(activity_id_list, rewarded):
        return user_activity_rewards_collection.update_many({"activity_id": {"$in": activity_id_list}}, {"$set": {"rewarded": rewarded}})