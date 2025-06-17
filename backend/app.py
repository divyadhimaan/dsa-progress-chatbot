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
    print("💬 Received request")
    data = request.get_json()
    print("📥 Data:", data)
    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"reply": "⚠️ Please enter a message."}), 400

    try:
        response = dsa_agent(user_input)
        return jsonify({"reply": response})
    except Exception as e:
        print("Error in dsa_agent:", str(e))
        return jsonify({"reply": "❌ Something went wrong on the server."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)