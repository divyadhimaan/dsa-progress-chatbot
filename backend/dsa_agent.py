import json
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import re
from pymongo import MongoClient
import certifi

from logger import (
    append_session_log
)

from dsa_schedule import *
load_dotenv()

        
def extract_days(text):
    matches = re.findall(r"day\s*(\d+)|(?<!\d)(\d+)(?!\d)", text.lower())
    return [int(num1 or num2) for num1, num2 in matches]
        
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
        days = extract_days(lower)
        if days:
            for day in days:
                unmark_day_completed(day)
            return f"❌ Unmarked Day(s): {', '.join(map(str, days))}."
        else:
            return "❓ Couldn't extract which day(s) to unmark. Try 'Unmark Day 3 and 4'."

    # 3. Mark day as completed
    if "day" in lower and "mark" in lower:
        days = extract_days(lower)
        if days:
            for day in days:
                mark_day_completed(day)
            return f"✅ Marked Day(s) completed: {', '.join(map(str, days))}."
        else:
            return "❓ Couldn't extract which day(s) to mark. Try 'Mark Day 3 and 4 as done'."

    # 4. Ask for a specific day’s plan
    if "day" in lower and any(k in lower for k in ["problem", "plan", "focus"]):
        days = extract_days(lower)
        if days:
            return get_day_plan(days[0])  # just show first matched
        else:
            return "❓ Couldn't find which day you want. Try 'Show Day 4’s plan'."

    # 5. General plan
    if "what" in lower and "plan" in lower:
        return get_next_day_plan()
    
    # 6. Show completed days (accurate version)
    if any(q in lower for q in ["show", "what", "list", "which"]) and "completed" in lower and "day" in lower:
        completed_days = sorted([int(day) for day in load_completed_days()])

        if not completed_days:
            return "📭 You haven't marked any days as completed yet. Let's get started!"

        

        df = load_schedule()
        print("Schedule columns:", df.columns.tolist())
        
        print("Completed days:", completed_days)
        print("Schedule days in df:", df["Day"].tolist())

        completed_df = df[df["Day"].isin(completed_days)]

        table_lines = [
            f"| Day | Topic | Questions |",
            f"|-----|--------|-----------|"
        ]
        for _, row in completed_df.iterrows():
            day = row.get("Day", "")
            topic = row.get("Focus", "Unknown")
            p1 = row.get("Problem 1", "")
            p2 = row.get("Problem 2", "")
            p3 = row.get("Problem 3", "")
            
            questions = [p1, p2, p3]

            # Optional: handle questions as list or string
            if isinstance(questions, list):
                questions_str = ", ".join(questions)
            else:
                questions_str = str(questions)

            table_lines.append(f"| {day} | {topic} | {questions_str} |")

        table_output = "\n".join(table_lines)
        return (
            f"✅ You've completed {len(completed_days)} day(s):\n\n"
            f"{table_output}"
        )
        
    # 7. How many days are left?
    if any(q in lower for q in ["how many", "what", "show"]) and any(k in lower for k in ["left", "remaining", "pending"]):
        df = load_schedule()
        total_days = df["Day"].nunique()
        completed = load_completed_days()
        remaining = total_days - len(completed)

        if remaining == 0:
            return "🎉 Woohoo! You've completed all the days in your DSA schedule!"
        return f"⏳ {remaining} day(s) left out of {total_days}. Keep pushing — you're doing great! 💪"

    # 8. Completed topics summary
    if any(k in lower for k in ["completed", "topics", "done"]):
        summary, _ = get_all_completed_topics()
        return summary

    # 9. Clear all progress
    if "clear" in lower:
        clear_progress()
        return "✅ All progress cleared."

    # 10. Fallback
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
        error_message = f"⚠️ Oops! My circuits tripped over a bug while trying to follow your command."
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


