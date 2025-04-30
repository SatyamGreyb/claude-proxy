from flask import Flask, request, jsonify, send_file
import requests
import os
import logging

app = Flask(__name__)

# Get API key from environment variable
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")

# Setup logging
logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    return "Claude Proxy API is up!"

@app.route("/claude", methods=["POST"])
def call_claude():
    data = request.json
    user_prompt = data.get("prompt", "")

    logging.info(f"[Prompt Received] {user_prompt}")

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
        reply = result.get("content", "No reply from Claude.")
        logging.info(f"[Claude Reply] {reply}")
        return jsonify({"reply": reply})
    except Exception as e:
        logging.error(f"[ERROR] {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/openapi.json")
def serve_openapi():
    return send_file("openapi.json", mimetype="application/json")
