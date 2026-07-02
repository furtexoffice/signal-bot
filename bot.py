import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Get token from environment variable
TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)
bot = Bot(token=TOKEN)

# Telegram command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is working!")

# Create telegram application
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Home route
@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
