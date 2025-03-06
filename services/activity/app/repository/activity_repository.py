from models.activity_model import activity_collection
from bson import ObjectId

class ActivityRepository:
    @staticmethod
    def create_activity(activity_data):
        """사용자 추가"""
        return activity_collection.insert_one(activity_data).inserted_id

    @staticmethod
    def find_activity_by_name(name):
        """이름으로 활동 조회"""
        return activity_collection.find_one({"name": name})

    @staticmethod
    def find_activity_by_ids(activity_ids):
        """id로 활동 조회"""
        if isinstance(activity_ids, str):  # 단일 문자열이 들어올 경우
            activity_ids = [activity_ids]

        # 문자열 ID를 ObjectId로 변환
        object_ids = [ObjectId(id) if ObjectId.is_valid(id) else id for id in activity_ids]

        return activity_collection.find({"_id": {"$in": object_ids}})

    @staticmethod
    def update_user_activity_rewards(reward_id_list):
        """사용자 활동 보상 업데이트"""
        return user_activity_rewards_collection.update_many({"_id": {"$in": reward_id_list}}, {"$set": {"rewarded": True}})