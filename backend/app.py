from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from dsa_agent import dsa_agent, get_session_logs, session_memory, persist_session_to_mongo


import json
import os

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:3000",           # for local dev
    "https://d-bot-jet.vercel.app"     # for production
]}})


@app.route("/")
def home():
    return "DSA Chatbot Backend is Running."

@app.route("/healthy", methods=["GET"])
def healthy():
    return "OK", 200

@app.route("/api/message", methods=["POST"])
def chat():

    print("💬 Received /api/message POST")
    if request.method == "OPTIONS":
        return jsonify({}), 200

    try:
        data = request.get_json()
        print("📥 Received:", data)

        message = data.get("message", "")
        model = data.get("model", "llama3-8b-8192")
        session_id = data.get("session_id")

        if not message:
            return jsonify({"reply": "⚠️ Message is missing."}), 400
        

        response = dsa_agent(user_input=message, model=model,session_id=session_id )
        return jsonify({"reply": response})

    except Exception as e:
        print("❌ Exception occurred:")
        traceback.print_exc()  # Logs full error trace
        return jsonify({"reply": "❌ Server error"}), 500
    
@app.route("/api/memory", methods=["GET"])
def get_memory():
    session_id = request.args.get("session_id")
    if not session_id:
        return jsonify([])

    return jsonify(get_session_logs(session_id))

    
@app.route("/api/clear", methods=["POST"])
def clear_memory():
    session_id = request.args.get("session_id")
    if not session_id:
        return jsonify({"status": "error", "message": "Missing session_id"}), 400

    persist_session_to_mongo(session_id)

    if session_id in session_memory:
        session_memory[session_id]["logs"] = []
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("BACKEND_PORT")  , debug=True)