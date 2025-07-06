# logger.py

from datetime import datetime
from pymongo import MongoClient, errors
import os
import certifi
import threading
import time

from dotenv import load_dotenv
load_dotenv()

use_mongo = True
session_memory = {}
PERSIST_INTERVAL_SECONDS = 300

try:
    MONGO_URI = os.environ.get("MONGO_URI")
    mongo_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=3000)
    mongo_client.server_info()  # Forces connection test
    db = mongo_client["dsa_memory"]
    logs_collection = db["logs"]
    print("✅ MongoDB connection established for logs.")
except errors.ServerSelectionTimeoutError:
    print("⚠️ MongoDB connection failed. Falling back to local logging.")
    use_mongo = False
    logs_collection = None

def periodic_persist():
    while True:
        print("⏳ Cron job triggered: Persisting all session logs...")
        for session_id in list(session_memory.keys()):
            persist_session_to_mongo(session_id)
        time.sleep(PERSIST_INTERVAL_SECONDS)

def start_cron_persist():
    thread = threading.Thread(target=periodic_persist, daemon=True)
    thread.start()
    print("🔄 Started background log persister thread.")
    
def get_session_logs(session_id):
    return session_memory.get(session_id, {}).get("logs", [])


def append_session_log(session_id, user_input, response):
    if session_id not in session_memory:
        session_memory[session_id] = {"logs": []}
    session_memory[session_id]["logs"].append({
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "response": response
    })


def persist_session_to_mongo(session_id):
    logs = get_session_logs(session_id)
    if not logs or not use_mongo or logs_collection is None:
        print("❌ Skipping Mongo persistence: logs missing or Mongo unavailable")
        return

    print(f"Persisting {len(logs)} logs for session {session_id} to MongoDB...")

    try:
        logs_collection.insert_one({
            "session_id": session_id,
            "created_at": datetime.now(),
            "logs": logs
        })
        session_memory[session_id]["logs"] = []
        print("✅ Successfully persisted logs to MongoDB")
    except Exception as e:
        print(f"❌ Failed to persist logs for session {session_id}: {e}")
