from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")

@app.route("/")
def home():
    return "Claude Proxy API is up!"

@app.route("/claude", methods=["POST"])
def call_claude():
    data = request.json
    user_prompt = data.get("prompt", "")

    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    payload = {
        "model": "claude-3-5-haiku-20241022",
        "messages": [{"role": "user", "content": user_prompt}],
        "max_tokens": 1024,
        "temperature": 0.7
    }

    try:
        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return jsonify({"reply": result.get("content", "No reply from Claude.")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
from flask import send_file

@app.route("/openapi.json")
def serve_openapi():
    return send_file("openapi.json", mimetype="application/json")
