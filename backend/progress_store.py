# progress_store.py

import json
import os
from pymongo import MongoClient, errors
import certifi
from dotenv import load_dotenv
from datetime import datetime


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
    print("✅ MongoDB connection established for progress.")

except errors.ServerSelectionTimeoutError:
    print("⚠️ MongoDB connection failed. Falling back to local file.")
    use_mongo = False


def get_progress_data():
    if use_mongo:
        doc = progress_collection.find_one({"_id": PROGRESS_DOC_ID})
        return doc.get("completed_days", {}) if doc else {}
    elif os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_progress_data(progress_dict):
    if use_mongo:
        progress_collection.update_one(
            {"_id": PROGRESS_DOC_ID},
            {"$set": {"completed_days": progress_dict}},
            upsert=True
        )
    else:
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress_dict, f, indent=2)


def load_completed_days():
    print("Loading completing days..")
    return get_progress_data()


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
def get_completed_day_list():
    """Returns a sorted list of completed day numbers"""
    progress = get_progress_data()
    return sorted(int(day) for day in progress.keys())