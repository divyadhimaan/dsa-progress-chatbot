import pandas as pd
import json
import os

from leetcode_map import LEETCODE_PROBLEMS


CSV_PATH = "dsa_sheet.csv"
PROGRESS_FILE = "completed_days.json"


# Load the CSV
def load_schedule():
    return pd.read_csv(CSV_PATH)

def load_completed_days():
    if not os.path.exists(PROGRESS_FILE):
        return set()
    with open(PROGRESS_FILE, "r") as f:
        return set(json.load(f))


# Get today's problems by day number
def get_day_plan(day):
    df = load_schedule()
    row = df[df["Day"]==day]
    if row.empty:
        return f"⚠️ Day {day} not found in the schedule."
    
    row = row.iloc[0]
    problems = [row["Problem 1"], row["Problem 2"], row["Problem 3"]]
    response = f"📅 Day {int(row['Day'])} — Focus: {row['Focus']}\n"
    for i, prob in enumerate(problems, 1):
        url = LEETCODE_PROBLEMS.get(prob)
        if url:
            response += f"- Problem {i}: [{prob}]({url})\n"
        else:
            response += f"- Problem {i}: {prob}\n"
    return response

def get_all_completed_topics():
    df = load_schedule()
    completed_df = load_completed_days()

    completed_topics = set()
    debug_log = []

    for _, row in df.iterrows():
        day_str = str(int(row["Day"]))
        topic = str(row["Focus"]).strip() if not pd.isna(row["Focus"]) else ""

        if day_str in completed_df and topic and topic.lower() != "(missing topic)":
            completed_topics.add(topic)
            debug_log.append(f"✔️ Day {day_str} — {topic}")
        else:
            debug_log.append(f"❌ Skipped Day {day_str} — Topic: {topic}")

    # Uncomment to debug
    # print("\n".join(debug_log))

    if not completed_topics:
        return "❗ You haven't completed any valid topics yet. Let’s start solving!", []

    sorted_topics = sorted(completed_topics)
    summary = (
        f"You've completed {len(sorted_topics)} topics so far. Keep going! 🚀\n\n"
        "Here are your completed topics:\n\n"
        + "\n".join(f"- {topic}" for topic in sorted_topics)
    )
    return summary, sorted_topics

def mark_day_completed(day):
    completed_df = load_completed_days()
    completed_df.add(str(day))
    with open(PROGRESS_FILE, "w") as f:
        json.dump(list(completed_df), f)
        
def unmark_day_completed(day):
    completed_df = load_completed_days()
    day_str = str(day)
    if day_str in completed_df:
        completed_df.remove(day_str)
        with open(PROGRESS_FILE, "w") as f:
            json.dump(list(completed_df), f)
    
def clear_progress():
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
    print("Progress has been cleared. Start again soon.")
    
def get_next_day_plan():
    df = load_schedule()
    completed_df = load_completed_days()

    
    for _, row in df.iterrows():
        day_str = str(int(row["Day"]))
        if day_str not in completed_df:
            response = get_day_plan(int(day_str))

            return response
        
    
    return "🎉 You’ve completed all days in your DSA schedule!"
    

if __name__ == "__main__":
    # print(get_day_plan(2))
    # print(get_todays_plan())
    # mark_day_completed(3)
    print(get_next_day_plan())