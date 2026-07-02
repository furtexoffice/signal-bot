import os
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

TOKEN = "8782499211:AAHidPUoe1Izg4j1dB6c1y6IcHSTS2mkhso"
bot = Bot(token=TOKEN)

app = Flask(__name__)

# Store user settings (simple version)
user_settings = {
    "timeframe": "5m"
}

# Start command
def start(update, context):
    update.message.reply_text(
        f"Welcome Temple ⚡\n\n"
        f"Current Timeframe: {user_settings['timeframe']}\n\n"
        f"Commands:\n"
        f"/timeframe 1m, 5m, 15m\n"
        f"/status"
    )

# Set timeframe
def set_timeframe(update, context):
    try:
        tf = context.args[0]
        user_settings["timeframe"] = tf
        update.message.reply_text(f"✅ Timeframe set to {tf}")
    except:
        update.message.reply_text("Usage: /timeframe 1m")

# Status
def status(update, context):
    update.message.reply_text(
        f"📊 Current Settings\nTimeframe: {user_settings['timeframe']}"
    )

# Webhook route (for TradingView later)
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.json

    pair = data.get("pair", "EURUSD")
    signal = data.get("signal", "BUY")

    message = (
        f"📊 SIGNAL ALERT\n\n"
        f"Pair: {pair}\n"
        f"Action: {signal}\n"
        f"Timeframe: {user_settings['timeframe']}\n\n"
        f"Trade now ⚡"
    )

    bot.send_message(chat_id=data.get("chat_id"), text=message)
    return "ok"

# Dispatcher
from telegram.ext import Updater

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("timeframe", set_timeframe))
dp.add_handler(CommandHandler("status", status))

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    from threading import Thread

    Thread(target=updater.start_polling).start()
    app.run(host="0.0.0.0", port=10000)