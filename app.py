import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

from chatbot_config import SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set.")

client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-3.1-flash-lite"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"reply": "Please enter a message."}), 400

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"{SYSTEM_PROMPT}\n\nUser message:\n{message}"
        )
        reply = response.text.strip() if response.text else "I couldn't generate a response."
        return jsonify({"reply": reply})
    except Exception as error:
        app.logger.exception("Gemini API error")
        return jsonify({
            "reply": "Sorry, I couldn't process your request right now."
        }), 500


if __name__ == "__main__":
    app.run()
