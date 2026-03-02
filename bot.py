import os
import requests
import datetime
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Token laden und säubern
TOKEN = os.getenv("TelegramToken", "").strip(" '\"")

REPOS = {
    "momentum": "Next-Flip/Momentum-Firmware",
    "unleashed": "DarkFlippers/unleashed-firmware"
}

start_time = datetime.datetime.now()

def get_github_release(repo_path):
    url = f"https://api.github.com/repos/{repo_path}/releases/latest"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        name = data.get("name", "N/A")
        link = data.get("html_url", "")
        return f"🚀 *{repo_path.split('/')[-1]}*\nName: {name}\nLink: {link}"
    except Exception as e:
        return f"Fehler beim Abrufen der Daten für {repo_path}."

async def momentum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = get_github_release(REPOS["momentum"])
    await update.message.reply_text(text, parse_mode=constants.ParseMode.MARKDOWN)

async def unleashed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = get_github_release(REPOS["unleashed"])
    await update.message.reply_text(text, parse_mode=constants.ParseMode.MARKDOWN)

async def protopirate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("https://ghcif.de/flipperzero/")

async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    delta = datetime.datetime.now() - start_time
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, _ = divmod(rem, 60)
    await update.message.reply_text(f"Bot läuft seit: {days} Tagen, {hours} Stunden, {minutes} Minuten")

async def hilfe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 *Verfügbare Befehle:*\n\n"
        "/momentum - Aktuelles Momentum Release\n"
        "/unleashed - Aktuelles Unleashed Release\n"
        "/protopirate - Link zur Protopirate Seite\n"
        "/uptime - Laufzeit des Bots\n"
        "/hilfe - Diese Übersicht"
    )
    await update.message.reply_text(help_text, parse_mode=constants.ParseMode.MARKDOWN)

if __name__ == '__main__':
    if not TOKEN:
        print("Fehler: Kein Token in .env gefunden.")
        exit(1)

    print("Python Bot startet im reaktiven Modus...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("momentum", momentum))
    app.add_handler(CommandHandler("unleashed", unleashed))
    app.add_handler(CommandHandler("protopirate", protopirate))
    app.add_handler(CommandHandler("uptime", uptime))
    app.add_handler(CommandHandler("hilfe", hilfe))

    print("Bot ist bereit.")
    app.run_polling()
