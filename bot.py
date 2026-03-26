import os
import requests
import datetime
import re
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants, LinkPreviewOptions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import NetworkError, TimedOut, Conflict, TelegramError

# Logging-Konfiguration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

TOKEN = os.getenv("TelegramToken", "").strip(" '\"")

REPOS = {
    "momentum": "Next-Flip/Momentum-Firmware",
    "unleashed": "DarkFlippers/unleashed-firmware",
    "arf": "D4C1-Labs/Flipper-ARF"
}

start_time = datetime.datetime.now()

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        raise context.error
    except Exception as e:
        logger.error(f"Systemfehler: {e}", exc_info=True)

def get_release_info(repo_path):
    url = f"https://api.github.com/repos/{repo_path}/releases/latest"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        name = data.get("name") or "N/A"
        link = data.get("html_url") or ""
        body = data.get("body") or ""
        
        # 1. HTML-Tags entfernen
        clean_body = re.sub('<[^<]+?>', '', body)
        # 2. Markdown-Links [Text](URL) zu nur "Text" vereinfachen
        clean_body = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_body)
        # 3. Rohe URLs entfernen (optional, für maximale Sauberkeit)
        clean_body = re.sub(r'http[s]?://\S+', '', clean_body)
        
        short_body = (clean_body[:250] + '...') if len(clean_body) > 250 else clean_body
        
        return {
            "name": name, 
            "link": link, 
            "body": short_body.strip(), 
            "repo": repo_path.split('/')[-1]
        }
    except Exception as e:
        logger.error(f"GitHub API Fehler ({repo_path}): {e}")
        return None

async def send_release(update: Update, repo_key: str):
    if not update.effective_message:
        return

    data = get_release_info(REPOS[repo_key])
    if not data:
        await update.effective_message.reply_text("Daten konnten nicht abgerufen werden.")
        return

    text = (f"🚀 *{data['repo']} Update*\n\n"
            f"📦 *Version:* `{data['name']}`\n\n"
            f"📝 *Changelog (Auszug):*\n_{data['body'] or 'Keine Details verfügbar.'}_")
    
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 Release auf GitHub", url=data['link'])]
    ])
    
    # Hier wird die Link-Vorschau GLOBAL für diese Nachricht deaktiviert
    await update.effective_message.reply_text(
        text, 
        parse_mode=constants.ParseMode.MARKDOWN, 
        reply_markup=reply_markup,
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )

async def momentum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_release(update, "momentum")

async def unleashed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_release(update, "unleashed")

async def arf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_release(update, "arf")

async def protopirate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message:
        await update.effective_message.reply_text(
            "🔗 [Protopirate - Flipper Zero Tools](https://ghcif.de/flipperzero/)", 
            parse_mode=constants.ParseMode.MARKDOWN,
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )

async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message:
        delta = datetime.datetime.now() - start_time
        await update.effective_message.reply_text(
            f"🔋 *Laufzeit:* {delta.days}d {delta.seconds//3600}h {(delta.seconds//60)%60}m", 
            parse_mode=constants.ParseMode.MARKDOWN
        )

async def hilfe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message:
        help_text = ("🤖 *Flipper Zero Release Bot*\n\n"
                     "/momentum - Aktuelles Momentum Release\n"
                     "/unleashed - Aktuelles Unleashed Release\n"
                     "/arf - Aktuelles ARF Release\n"
                     "/protopirate - Link zur gepachten Protopirate Fap\n"
                     "/uptime - Laufzeit des Bots\n"
                     "/hilfe - Diese Übersicht")
        await update.effective_message.reply_text(
            help_text, 
            parse_mode=constants.ParseMode.MARKDOWN, 
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )

if __name__ == '__main__':
    if not TOKEN:
        logger.critical("Token fehlt.")
        exit(1)

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_error_handler(error_handler)

    app.add_handler(CommandHandler("momentum", momentum))
    app.add_handler(CommandHandler("unleashed", unleashed))
    app.add_handler(CommandHandler("arf", arf))
    app.add_handler(CommandHandler("protopirate", protopirate))
    app.add_handler(CommandHandler("uptime", uptime))
    app.add_handler(CommandHandler("hilfe", hilfe))

    logger.info("Bot-Instanz gestartet.")
    app.run_polling()
