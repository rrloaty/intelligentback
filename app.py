from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ⚠️ Keep your bot token safe here (never in frontend)
BOT_TOKEN = "8433235666:AAGUgGfrFwj5dvE548wxyIpyzjrlaWXu_VA"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route("/", methods=["GET"])
def home():
    return "✅ Telegram Form Backend is running!"

@app.route("/send", methods=["POST"])
def send():
    try:
        data = request.json
        chat_id = data.get("chat_id")
        text = data.get("text")

        if not chat_id or not text:
            return jsonify({"ok": False, "error": "chat_id and text required"}), 400

        res = requests.post(TELEGRAM_API, json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        })

        return jsonify(res.json())

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)