from openai import OpenAI
import json
from datetime import datetime
from dotenv import load_dotenv
import os

from dsa_schedule import get_day_plan, mark_day_completed, get_next_day_plan, load_completed_days, get_all_completed_topics, clear_progress


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


MEMORY_FILE = "memory.json"
try:
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
except:
    memory = {"logs": []}

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


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
    
    if "completed" in lower or "topics" in lower:
        return get_all_completed_topics()
    
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

    # try:
    #     messages = [
    #         {
    #             "role": "system",
    #             "content": (
    #                 "You're Divya's DSA preparation assistant. "
    #                 "Track progress, suggest topics, answer interview prep questions, and stay positive and motivating."
    #             )
    #         },
    #         {
    #             "role": "user",
    #             "content": user_input
    #         }
    #     ]

    #     # Call OpenAI
    #     response = client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=messages
    #     )

    #     reply = response.choices[0].message.content

    #     # Save to memory if it's a progress log
    #     if any(word in user_input.lower() for word in ["solved", "did", "completed", "finished"]):
    #         memory["logs"].append({
    #             "timestamp": str(datetime.now()),
    #             "entry": user_input
    #         })
    #         save_memory()

    # except Exception as e:
    #     print("❌ OpenAI call failed, returning mock response:", str(e))

    return reply