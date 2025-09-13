from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend (GitHub Pages, etc.) can call backend

BOT_TOKEN = "8433235666:AAGUgGfrFwj5dvE548wxyIpyzjrlaWXu_VA"

@app.route("/submit", methods=["POST"])
def submit_form():
    data = request.json

    # Extract form details
    user_id = data.get("userId")
    page_title = data.get("pageTitle", "No Title")
    form_name = data.get("formName", "Unnamed Form")

    # Build message for Telegram
    message = f"📄 Page: {page_title}\n📝 Form: {form_name}\n\n"
    for k, v in data.items():
        if k not in ["userId", "pageTitle", "formName"]:
            message += f"{k}: {v}\n"

    # Send to Telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(url, json={"chat_id": user_id, "text": message})

    if resp.status_code == 200:
        return jsonify({"status": "success"})
    else:
        return jsonify({"error": resp.text}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)