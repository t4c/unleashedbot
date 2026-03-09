import os
import requests
import datetime
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Token laden
TOKEN = os.getenv("TelegramToken", "").strip(" '\"")

# Konfiguration
REPOS = {
    "momentum": "Next-Flip/Momentum-Firmware",
    "unleashed": "DarkFlippers/unleashed-firmware"
}

start_time = datetime.datetime.now()

def get_release_info(repo_path):
    """Holt Release-Daten und bereitet sie auf."""
    url = f"https://api.github.com/repos/{repo_path}/releases/latest"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        name = data.get("name", "N/A")
        link = data.get("html_url", "")
        body = data.get("body", "")
        
        # Säubert den Text und kürzt auf 250 Zeichen
        clean_body = re.sub('<[^<]+?>', '', body)
        short_body = (clean_body[:250] + '...') if len(clean_body) > 250 else clean_body
        
        return {
            "name": name,
            "link": link,
            "body": short_body,
            "repo": repo_path.split('/')[-1]
        }
    except Exception as e:
        print(f"Fehler bei {repo_path}: {e}")
        return None

async def send_release(update: Update, repo_key: str):
    """Generische Funktion zum Senden der Release-Infos."""
    data = get_release_info(REPOS[repo_key])
    if not data:
        await update.message.reply_text("Fehler beim Abrufen der GitHub-Daten.")
        return

    text = (
        f"🚀 *{data['repo']} Update*\n\n"
        f"📦 *Version:* `{data['name']}`\n\n"
        f"📝 *Changelog (Auszug):*\n_{data['body']}_"
    )
    
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 Release auf GitHub", url=data['link'])]
    ])
    
    await update.message.reply_text(
        text, 
        parse_mode=constants.ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )

async def momentum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_release(update, "momentum")

async def unleashed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_release(update, "unleashed")

async def protopirate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔗 [Protopirate - Flipper Zero Tools](https://ghcif.de/flipperzero/)", parse_mode=constants.ParseMode.MARKDOWN)

async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    delta = datetime.datetime.now() - start_time
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, _ = divmod(rem, 60)
    await update.message.reply_text(f"🔋 *Laufzeit:* {days}d {hours}h {minutes}m", parse_mode=constants.ParseMode.MARKDOWN)

async def hilfe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 *Flipper Zero Release Bot*\n\n"
        "/momentum - Aktuelles Momentum Release\n"
        "/unleashed - Aktuelles Unleashed Release\n"
        "/protopirate - Link zur gepachten Protopirate Fap\n"
        "/uptime - Laufzeit des Bots\n"
        "/hilfe - Diese Übersicht"
    )
    await update.message.reply_text(help_text, parse_mode=constants.ParseMode.MARKDOWN, disable_web_page_preview=True)

if __name__ == '__main__':
    if not TOKEN:
        print("CRITICAL: Kein Token gefunden!")
        exit(1)

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("momentum", momentum))
    app.add_handler(CommandHandler("unleashed", unleashed))
    app.add_handler(CommandHandler("protopirate", protopirate))
    app.add_handler(CommandHandler("uptime", uptime))
    app.add_handler(CommandHandler("hilfe", hilfe))

    print("Bot läuft...")
    app.run_polling()
