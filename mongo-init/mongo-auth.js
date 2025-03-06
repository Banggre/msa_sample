db = db.getSiblingDB("volunteer_db");  

if (!db.getCollectionNames().includes("users")) {
    db.createCollection("users");
}

var userSchema = {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["email", "password"],
            properties: {
                email: {
                    bsonType: "string",
                    description: "user email (required)"
                },
                password: {
                    bsonType: "string",
                    description: "password (required)"
                }
            }
        }
    }
};

db.runCommand({
    collMod: "users",
    validator: userSchema.validator
});

db.users.insertMany([
    { _id: ObjectId("67c6b619784675d56ee21e53"), email: "testuser@naver.com", password: "testpass" },
    { _id: ObjectId("67c6b72b99d74e34800ba5f7"), email: "testuser2@naver.com", password: "testpass2" }
]);