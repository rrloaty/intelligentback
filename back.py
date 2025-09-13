from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BOT_TOKEN = "8433235666:AAGUgGfrFwj5dvE548wxyIpyzjrlaWXu_VA"

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    chat_id = data.get("chat_id")
    text = data.get("text")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, json={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    })
    return jsonify(r.json())
