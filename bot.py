import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler
# Secure token (from Render environment variable)
TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=TOKEN)
app = Flask(__name__)

# Store user settings
user_settings = {
    "timeframe": "5m"
}

# ---------------- COMMANDS ---------------- #

def start(update, context):
    update.message.reply_text(
        f"Welcome Temple ⚡\n\n"
        f"Current Timeframe: {user_settings['timeframe']}\n\n"
        f"Commands:\n"
        f"/timeframe 1m, 5m, 15m\n"
        f"/status"
    )

def status(update, context):
    update.message.reply_text(
        f"⚙️ Current Settings:\n"
        f"Timeframe: {user_settings['timeframe']}"
    )

def set_timeframe(update, context):
    try:
        tf = context.args[0]

        if tf not in ["1m", "5m", "15m"]:
            update.message.reply_text("❌ Invalid timeframe. Use 1m, 5m, or 15m")
            return

        user_settings["timeframe"] = tf
        update.message.reply_text(f"✅ Timeframe set to {tf}")

    except:
        update.message.reply_text("⚠️ Usage: /timeframe 1m or 5m or 15m")

# ---------------- DISPATCHER ---------------- #

application = Application.builder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))
application.add_handler(CommandHandler("timeframe", set_timeframe))
# ---------------- FLASK ROUTES ---------------- #

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.process_update(update)
    return "ok"

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
