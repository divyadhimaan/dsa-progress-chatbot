# progress_store.py

import json
import os
from pymongo import MongoClient, errors
import certifi
from dotenv import load_dotenv

load_dotenv()

PROGRESS_FILE = "completed_days.json"
PROGRESS_DOC_ID = "progress_tracker"

use_mongo = True
try:
    MONGO_URI = os.environ.get("MONGO_URI")
    mongo_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=3000)
    mongo_client.server_info()
    db = mongo_client["dsa_memory"]
    progress_collection = db["progress"]
except errors.ServerSelectionTimeoutError:
    print("⚠️ MongoDB connection failed. Falling back to local file.")
    use_mongo = False


def load_completed_days():
    print("Loading completing days..")
    if use_mongo:
        doc = progress_collection.find_one({"_id": PROGRESS_DOC_ID})
        if doc and "completed_days" in doc:
            return set(doc["completed_days"])
        return set()
    else:
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, "r") as f:
                return set(json.load(f))
        return set()


def save_completed_days(days_set):
    print("Saving completed days: ", days_set)

    if use_mongo:
        progress_collection.update_one(
            {"_id": PROGRESS_DOC_ID},
            {"$set": {"completed_days": list(days_set)}},
            upsert=True
        )
    else:
        with open(PROGRESS_FILE, "w") as f:
            json.dump(list(days_set), f)
