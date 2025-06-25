import pandas as pd
import json
import os
from datetime import datetime


from leetcode_map import LEETCODE_PROBLEMS
from progress_store import load_completed_days, get_completed_day_list, save_progress_data


CSV_PATH = "dsa_sheet.csv"


# Load the CSV
def load_schedule():
    return pd.read_csv(CSV_PATH)


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
    print("getting all completed topics: ")
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
        + ", ".join(f"{topic}" for topic in sorted_topics)
    )
    return summary, sorted_topics

# def mark_day_completed(day):
#     completed = load_completed_days()  # returns dict {day: timestamp}
#     completed[str(day)] = datetime.now().isoformat()
#     save_progress_data(completed)  # save back to file or Mongo
#     print(f"✅ Marked Day {day} as completed with timestamp.")
    
def mark_day_completed(day):
    df = load_schedule()
    row = df[df["Day"] == day]
    
    if row.empty:
        print(f"⚠️ Day {day} not found in schedule.")
        return
    
    topic = str(row.iloc[0]["Focus"]).strip()
    completed = load_completed_days()

    completed[str(day)] = {
        "timestamp": datetime.now().isoformat(),
        "topic": topic if topic else "Unknown"
    }

    save_progress_data(completed)
    print(f"✅ Marked Day {day} as completed — Topic: {topic}")
        
# def unmark_day_completed(day):
#     completed = load_completed_days()
#     day_str = str(day)
#     if day_str in completed:
#         del completed[day_str]
#         save_progress_data(completed)
#         print(f"❌ Unmarked Day {day} as completed.")

def unmark_day_completed(day):
    completed = load_completed_days()
    day_str = str(day)
    if day_str in completed:
        del completed[day_str]
        save_progress_data(completed)
        print(f"❌ Unmarked Day {day} as completed.")
    
def clear_progress():
    save_progress_data({})
    print("✅ Progress has been cleared. Start again soon.")
    
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