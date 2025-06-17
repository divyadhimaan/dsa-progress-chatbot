from backend.dsa_agent import dsa_agent

print("🧠 DSA Agent Initialized. Type 'exit' to stop.")
while True:
    user_input = input("👤 You: ")
    if user_input.lower() == "exit":
        break
    response = dsa_agent(user_input)
    print(f"🤖 Agent: {response}")
