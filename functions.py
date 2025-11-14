from fastapi import HTTPException
from pymongo import MongoClient
from bson import ObjectId
from models import User
from fastapi.responses import JSONResponse
import random
# Connect to MongoDB
client = MongoClient("mongodb+srv://usman:Us%4026618@cluster0.okzi335.mongodb.net/")
db = client["mydatabase"]
collection = db["newquestions"]
users_collection = db["users"]
config_collection = db["config"]
# --- Helper to make ObjectId JSON serializable ---
def serialize_doc(doc):
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

def get_questions():
    try:
        config = config_collection.find_one({"_id": "default_config"})
        if not config:
            return {"error": "default_config not found"}

        quiz = []

        # Loop through each subject defined in config
        for subj in config["subjects"]:
            subject_name = subj["name"]
            for q_type in subj["types"]:
                qtype = q_type["type"]
                for lvl in q_type["levels"]:
                    level_name = lvl["level"]
                    count = lvl["count"]

                    # Fetch questions from the questions collection
                    all_questions = list(collection.find({
                        "subject": subject_name,
                        "type": qtype,
                        "level": level_name
                    }))

                    # Randomly pick the required number of questions
                    if len(all_questions) > count:
                        selected = random.sample(all_questions, count)
                    else:
                        selected = all_questions  # if not enough questions, take all

                    quiz.extend([serialize_doc(q) for q in selected])

        return {"quiz": quiz, "total_questions": len(quiz)}

    except Exception as e:
        return {"error fetching questions": str(e)}
        
    
def add_user_to_db(user: User):
    if users_collection.find_one({"cnic": user.cnic}):
        return JSONResponse(status_code=400, content={"message": "User already exists"})

    users_collection.insert_one(user.dict())
    return {"message": "User added successfully", "data": user.dict()}

def add_user_result_to_db(result):
    # Check if the user exists using their number
    user = users_collection.find_one({"cnic": result.cnic})
    
    if user:
        # ✅ Use update_one instead of insert_one
        users_collection.update_one(
            {"cnic": result.cnic},             # find user by number
            {"$set": {"result": result.result, "total": result.total}}   # update or add 'result' field
        )
        return {"message": "Result added successfully"}
    else:
        return {"error": "User not found"}

def get_users():
    try:
        # Fetch users and remove _id from every document
        users = list(users_collection.find({}, {"_id": 0}))

        return {
            "status": "success",
            "total_users": len(users),
            "users": users
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
# delete user by cnic
def delete_user(cnic):
    try:
        result = users_collection.delete_one({"cnic": cnic})

        if result.deleted_count == 1:
            return {"status": "success", "message": "User deleted successfully"}
        else:
            return {"status": "error", "message": "User not found"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
