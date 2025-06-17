from flask import Flask, request, jsonify
from flask_cors import CORS
from dsa_agent import dsa_agent

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route("/")
def home():
    return "DSA Chatbot Backend is Running."

@app.route("/api/message", methods=["POST"])
def chat():

    print("💬 Received /api/message POST")
    if request.method == "OPTIONS":
        return jsonify({}), 200

    try:
        data = request.get_json()
        print("📥 Received:", data)

        message = data.get("message", "")
        if not message:
            return jsonify({"reply": "⚠️ Message is missing."}), 400

        response = dsa_agent(message)
        return jsonify({"reply": response})

    except Exception as e:
        print("❌ Exception occurred:")
        traceback.print_exc()  # Logs full error trace
        return jsonify({"reply": "❌ Server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)