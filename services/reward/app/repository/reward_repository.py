from models.reward_model import reward_collection

class RewardRepository:
    @staticmethod
    def find_reward_by_name(name):
        return reward_collection.find_one({"name": name})

    @staticmethod
    def update_reward_by_user_id(user_id, point):
        reward = reward_collection.find_one({"user_id": user_id})
        if reward:
            return reward_collection.update_one({"user_id": user_id}, {"$inc": {"point": point}})
        else:
            return reward_collection.insert_one({"user_id": user_id, "point": point}).inserted_id
