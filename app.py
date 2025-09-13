from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # <<< This is the key to fix the network error

BOT_TOKEN = os.getenv("BOT_TOKEN", "8433235666:AAGUgGfrFwj5dvE548wxyIpyzjrlaWXu_VA")

@app.route("/")
def home():
    return "✅ Backend running!"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    chat_id = data.get("chat_id")
    form_data = data.get("form_data", {})

    msg = f"📄 Page: {data.get('pageTitle', 'No Title')}\n📝 Form: {data.get('formName', 'Unnamed')}\n\n"
    for k, v in form_data.items():
        msg += f"{k}: {v}\n"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    res = requests.post(url, json={"chat_id": chat_id, "text": msg})

    if res.status_code == 200:
        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({"status": "error", "details": res.text}), 400