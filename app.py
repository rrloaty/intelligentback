from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8433235666:AAGUgGfrFwj5dvE548wxyIpyzjrlaWXu_VA")

@app.route("/")
def home():
    return "Server running!"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    chat_id = data.get("chat_id")
    form_data = data.get("form_data", {})

    # Format message
    msg = "📩 New Form Submission\n\n"
    for k, v in form_data.items():
        msg += f"{k}: {v}\n"

    # Send to Telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    res = requests.post(url, json={"chat_id": chat_id, "text": msg})

    if res.status_code == 200:
        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({"status": "error", "details": res.text}), 400