db = db.getSiblingDB("activity_db");  // 데이터베이스 선택

// "activity" 컬렉션이 존재하지 않으면 생성
if (!db.getCollectionNames().includes("activities")) {
    db.createCollection("activities");
}

// JSON Schema를 사용하여 "activity" 컬렉션의 스키마 정의
var activitySchema = {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["name", "type"],
            properties: {
                name: {
                    bsonType: "string",
                    description: "activity name (required)"
                },
                type: {
                    bsonType: "string",
                    enum: ["Volunteering", "Adoption"],
                    description: "activity type volunteering/adoption (required)"
                }
            }
        }
    }
};

// "activity" 컬렉션 스키마 적용
db.runCommand({
    collMod: "activities",
    validator: activitySchema.validator
});

// 기본 데이터 삽입 (ObjectId 설정)
db.activity.insertMany([
    { _id: ObjectId("67c6dda01f9f2aeffb717acd"), name: "Animal Shelter Visit", type: "Volunteering" },
    { _id: ObjectId("67c6df6f2ae3be91a4dc7338"), name: "Adopting a Pet", type: "Adoption" }
]);
// ======
if (!db.getCollectionNames().includes("user_activity_rewards")) {
    db.createCollection("user_activity_rewards");
}

// JSON Schema를 사용하여 "user_activity_rewards" 컬렉션의 스키마 정의
var userActivityRewardsSchema = {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["user_id", "activity_id"],
            properties: {
                user_id: {
                    bsonType: "string",
                    description: "user_id (required)"
                },
                activity_id: {
                    bsonType: "string",
                    description: "activity_id (required)"
                },
                rewarded: {
                    bsonType: "bool",
                    description: "rewarded"
                },
                created_at: {
                    bsonType: "date",
                    description: "created date"
                }
            }
        }
    }
};

// "user_activity_rewards" 컬렉션 스키마 적용
db.runCommand({
    collMod: "user_activity_rewards",
    validator: userActivityRewardsSchema.validator
});

// 기본 데이터 삽입 (ObjectId 설정)
db.user_activity_rewards.insertMany([
    { 
        "user_id": "67c6b619784675d56ee21e53",
        "activity_id": "67c6df6f2ae3be91a4dc7338",
        "rewarded": false,
        created_at: new Date()
    },
    { 
        "user_id": "67c6b619784675d56ee21e53",
        "activity_id": "67c6df6f2ae3be91a4dc7338",
        "rewarded": true,
        created_at: new Date()
    },
    { 
        "user_id": "67c6b619784675d56ee21e53",
        "activity_id": "67c6dda01f9f2aeffb717acd",
        "rewarded": false,
        created_at: new Date()
    },
    { 
        "user_id": "67c6b619784675d56ee21e53",
        "activity_id": "67c6dda01f9f2aeffb717acd",
        "rewarded": false,
        created_at: new Date()
    },
    { 
        "user_id": "67c6b619784675d56ee21e53",
        "activity_id": "67c6dda01f9f2aeffb717acd",
        "rewarded": false,
        created_at: new Date()
    },
    { 
        "user_id": "67c6b619784675d56ee21e53",
        "activity_id": "67c6dda01f9f2aeffb717acd",
        "rewarded": true,
        created_at: new Date()
    }
]);