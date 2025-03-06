from models.reward_model import rewards_collection

class RewardRepository:
    @staticmethod
    def find_reward_by_name(name):
        return rewards_collection.find_one({"name": name})

    @staticmethod
    def update_reward_by_user_id(user_id, point):
        reward = rewards_collection.find_one({"user_id": user_id})
        if reward:
            return rewards_collection.update_one({"user_id": user_id}, {"$inc": {"point": point}})
        else:
            return rewards_collection.insert_one({"user_id": user_id, "point": point}).inserted_id