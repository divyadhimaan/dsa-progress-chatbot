from openai import OpenAI
import json
from datetime import datetime
from dotenv import load_dotenv
import os
import requests

from dsa_schedule import get_day_plan, mark_day_completed, get_next_day_plan, load_completed_days, get_all_completed_topics, clear_progress


load_dotenv()


MEMORY_FILE = "memory.json"
try:
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
except:
    memory = {"logs": []}

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
        
def summarize_progress():
    summary, topics = get_all_completed_topics()
    return f"You've completed {len(topics)} topics:\n" + "\n".join(f"{i+1}. {topic}" for i, topic in enumerate(topics))

def interpret_input(user_input):
    lower = user_input.lower()

    if "today" in lower or "next" in lower:
        return get_next_day_plan()

    if "day" in lower and "mark" in lower:
        # e.g., "mark day 2 as done"
        import re
        match = re.search(r"day (\d+)", lower)
        if match:
            day = int(match.group(1))
            mark_day_completed(day)
            return f"✅ Day {day} marked as completed."
        else:
            return "❓ Couldn't extract which day to mark. Try 'Mark Day 3 as done'."

    if "day" in lower and ("problem" in lower or "plan" in lower or "focus" in lower):
        import re
        match = re.search(r"day (\d+)", lower)
        if match:
            day = int(match.group(1))
            return get_day_plan(day)
        else:
            return "❓ Couldn't find which day you want. Try 'Show Day 4’s plan'."

    if "what" in lower and "plan" in lower:
        return get_next_day_plan()
    
    if "completed" in lower or "topics" in lower or "done" in lower:
        summary, _ = get_all_completed_topics()
        return summary
    
    if "clear" in lower:
        clear_progress()
        return "✅ All progress cleared."
        

    return None  # fallback to OpenAI

def dsa_agent(user_input):
    # System prompt = agent persona
    try:
        structured_response = interpret_input(user_input)
        if structured_response:
            return structured_response
    except Exception as e:
        print("❌ interpret_input failed:", e)
        
    reply = f"🧪 Mock response for: '{user_input}'"
    
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")  
    if not GROQ_API_KEY:
        return "❌ Missing GROQ_API_KEY in environment variables."
    
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
        "model": "llama3-8b-8192",  # Or llama3-70b-8192 for more reasoning
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
    except requests.exceptions.HTTPError as e:
        print("❌ HTTP Error:", e.response.status_code, e.response.text)
        reply = "❌ Groq API call failed: HTTP error."
    except Exception as e:
        print("❌ Groq call failed:", str(e))
        reply = "❌ Groq API call failed."

    

    return reply


