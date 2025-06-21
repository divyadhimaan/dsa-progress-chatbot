import json
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import re
from pymongo import MongoClient
import certifi


from dsa_schedule import *


load_dotenv()

# Initialize MongoDB client for persistent memory
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = mongo_client["dsa_memory"]
logs_collection = db["logs"]

session_memory = {}

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
    
def get_session_history(session_id):
    logs = get_session_logs(session_id)
    return "\n".join(f"{log['timestamp']} - {log['user_input']} → {log['response']}" for log in logs)

def persist_session_to_mongo(session_id):
    logs = get_session_logs(session_id)
    if not logs:
        return
    
    print(f"Persisting {len(logs)} logs for session {session_id} to MongoDB...")
    
    try:
        logs_collection.insert_one({
            "session_id": session_id,
            "created_at": datetime.now(),
            "logs": logs
        })
        print("✅ Successfully persisted logs to MongoDB")
    except Exception as e:
        print(f"❌ Failed to persist logs for session {session_id}: {e}")

        
def extract_day(text):
    match = re.search(r"day (\d+)", text.lower())
    return int(match.group(1)) if match else None
        
def summarize_progress():
    summary, topics = get_all_completed_topics()
    return f"You've completed {len(topics)} topics:\n" + "\n".join(f"{i+1}. {topic}" for i, topic in enumerate(topics))

def interpret_input(user_input):
    lower = user_input.lower()

    # 1. Next day plan
    if "today" in lower or "next" in lower:
        return get_next_day_plan()

    # 2. Unmark day as completed
    if "day" in lower and (
        ("mark" in lower and "not" in lower) or
        "unmark" in lower or
        "uncompleted" in lower or
        "incomplete" in lower
    ):
        day = extract_day(lower)
        if day:
            unmark_day_completed(day)
            return f"❌ Day {day} marked as not completed."
        else:
            return "❓ Couldn't extract which day to unmark. Try 'Unmark Day 3'."

    # 3. Mark day as completed
    if "day" in lower and "mark" in lower:
        day = extract_day(lower)
        if day:
            mark_day_completed(day)
            return f"✅ Day {day} marked as completed."
        else:
            return "❓ Couldn't extract which day to mark. Try 'Mark Day 3 as done'."

    # 4. Ask for a specific day’s plan
    if "day" in lower and any(k in lower for k in ["problem", "plan", "focus"]):
        day = extract_day(lower)
        if day:
            return get_day_plan(day)
        else:
            return "❓ Couldn't find which day you want. Try 'Show Day 4’s plan'."

    # 5. General plan
    if "what" in lower and "plan" in lower:
        return get_next_day_plan()

    # 6. Completed topics summary
    if any(k in lower for k in ["completed", "topics", "done"]):
        summary, _ = get_all_completed_topics()
        return summary

    # 7. Clear all progress
    if "clear" in lower:
        clear_progress()
        return "✅ All progress cleared."

    # 8. Fallback
    return None

def dsa_agent(user_input, session_id=None, model="llama3-8b-8192"):
    # System prompt = agent persona
    try:
        structured_response = interpret_input(user_input)
        if structured_response:

            if session_id:
                append_session_log(session_id, user_input, structured_response)
                
            return {
                "status": "ok",
                "message": structured_response
            }
    except Exception as e:
        print("❌ interpret_input failed:", e)
        error_message = f"⚠️ Sorry! Something went wrong understanding your request.\n{str(e)}"
        if session_id:
            append_session_log(session_id, user_input, error_message)
        return {
            "status": "error",
            "message": error_message,
            "snackbar": "Some messages might be missing due to an internal error."
        }
        
    reply = f"🧪 Mock response for: '{user_input}'"
    
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")  
    if not GROQ_API_KEY:
        error_message = "❌ Missing GROQ_API_KEY in environment variables."
        if session_id:
            append_session_log(session_id, user_input, error_message)
        return {
            "status": "error",
            "message": error_message,
            "snackbar": "Internal configuration error. Please check environment setup."
        }
    
    messages = [
        {
            "role": "system",
            "content": (
                "You're Divya's DSA bot aka D-bot "
                "Track progress, suggest topics, answer interview prep questions, and stay positive and motivating."
                "Only rely on the provided list for completed topics. Do not make up extra content.\n"
                "When asked for completion progress, check completed topics\n"
                f"Current completed topics:\n{summarize_progress()}"
            )
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        if session_id:
            append_session_log(session_id, user_input, reply)
        return {
            "status": "ok",
            "message": reply
        }
    except requests.exceptions.HTTPError as e:
        print("❌ HTTP Error:", e.response.status_code, e.response.text)
        error_message = "❌ Groq API call failed: HTTP error."
    except Exception as e:
        print("❌ Groq call failed:", str(e))
        error_message = "❌ Groq API call failed."


    if session_id:
        append_session_log(session_id, user_input, error_message)
    return {
        "status": "error",
        "message": error_message,
        "snackbar": "LLM backend failed. Please try again later."
    }


