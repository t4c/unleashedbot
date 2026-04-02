import os
import httpx
import datetime
import re
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants, LinkPreviewOptions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

TOKEN = os.getenv("TelegramToken", "").strip(" '\"")
PROTOPIRATE_JSON = "https://ghcif.de/flipperzero/version.json"
PROTOPIRATE_DOWNLOAD = "https://ghcif.de/flipperzero/"

REPOS = {
    "momentum": "Next-Flip/Momentum-Firmware",
    "unleashed": "DarkFlippers/unleashed-firmware",
    "arf": "D4C1-Labs/Flipper-ARF"
}

start_time = datetime.datetime.now()

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Globaler Bot-Fehler: %s", context.error)

def get_user_log_info(update: Update):
    user = update.effective_user
    if not user: return "Unbekannter User"
    name = user.first_name
    username = f" (@{user.username})" if user.username else ""
    return f"{name}{username} [ID: {user.id}]"

def clean_momentum_changelog(body):
    if not body: return ""
    sections = re.split(r'(?m)^##\s+', body)
    relevant_parts = []
    blacklist_headers = ["download", "support", "donate", "donating", "install", "how to", "word"]
    blacklist_content = ["ko-fi", "paypal", "btc", "eth", "1EnCi1", "spread the word"]

    for section in sections:
        lines = section.split('\n')
        header = lines[0].lower().strip()
        if any(word in header for word in blacklist_headers): continue
        section_content = [line for line in lines[1:] if not any(word in line.lower() for word in blacklist_content)]
        clean_section = "\n".join(section_content).strip()
        if clean_section: relevant_parts.append(clean_section)
    return "\n".join(relevant_parts).strip()

def final_cleanup(text):
    if not text: return ""
    text = re.sub('<[^<]+?>', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'http[s]?://\S+', '', text)
    text = text.replace('>', '').replace('#', '').replace('**', '').replace('__', '').strip()
    text = re.sub(r'\n\s*\n', '\n', text)
    return (text[:350] + '...') if len(text) > 350 else text

async def get_release_info(repo_key):
    repo_path = REPOS[repo_key]
    url = f"https://api.github.com/repos/{repo_path}/releases/latest"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            body = data.get("body", "")
            if repo_key == "momentum": body = clean_momentum_changelog(body)
            return {"name": data.get("name") or "N/A", "link": data.get("html_url") or "", "body": final_cleanup(body), "repo": repo_path.split('/')[-1]}
        except Exception as e:
            logger.error("GitHub API Fehler (%s): %s", repo_path, e)
            return None

async def get_protopirate_custom_info():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(PROTOPIRATE_JSON, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error("Abfrage version.json fehlgeschlagen: %s", e)
            return None

async def send_release(update: Update, repo_key: str):
    if not update.effective_message: return
    logger.info("Befehl /%s von %s empfangen.", repo_key, get_user_log_info(update))
    await update.effective_chat.send_action(action=constants.ChatAction.TYPING)
    data = await get_release_info(repo_key)
    if not data:
        await update.effective_message.reply_text("Daten konnten nicht abgerufen werden.")
        return
    text = f"🚀 *{data['repo']} Update*\n\n📦 *Version:* `{data['name']}`\n\n📝 *Changelog (Auszug):*\n_{data['body'] or 'Keine Details verfügbar.'}_"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("📥 Release auf GitHub", url=data['link'])]])
    await update.effective_message.reply_text(text, parse_mode=constants.ParseMode.MARKDOWN, reply_markup=reply_markup, link_preview_options=LinkPreviewOptions(is_disabled=True))

async def momentum(u, c): await send_release(u, "momentum")
async def unleashed(u, c): await send_release(u, "unleashed")
async def arf(u, c): await send_release(u, "arf")

async def protopirate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message: return
    logger.info("Befehl /protopirate von %s empfangen.", get_user_log_info(update))
    await update.effective_chat.send_action(action=constants.ChatAction.TYPING)
    data = await get_protopirate_custom_info()
    if data:
        v = data.get('version', 'N/A')
        t = data.get('build_time', 'Unbekannt')
        c = data.get('changelog', 'Keine Details verfügbar.')
        text = (f"🏴‍☠️ *ProtoPirate Build*\n\n"
                f"📦 *Version:* `{v}`\n"
                f"📅 *Erstellt am:* {t}\n\n"
                f"📝 *Changelog (Auszug):*\n_{final_cleanup(c)}_")
    else:
        text = "🏴‍☠️ *ProtoPirate*\n\nHier findest du die aktuellsten FAPs inklusive Emulation-Patch."

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("📥 Download (ghcif.de)", url=PROTOPIRATE_DOWNLOAD)]])
    await update.effective_message.reply_text(text, parse_mode=constants.ParseMode.MARKDOWN, reply_markup=reply_markup, link_preview_options=LinkPreviewOptions(is_disabled=True))

async def uptime(update, context):
    logger.info("Befehl /uptime von %s empfangen.", get_user_log_info(update))
    delta = datetime.datetime.now() - start_time
    await update.effective_message.reply_text(f"🔋 *Laufzeit:* {delta.days}d {delta.seconds//3600}h {(delta.seconds//60)%60}m", parse_mode=constants.ParseMode.MARKDOWN)

async def hilfe(update, context):
    logger.info("Befehl /hilfe von %s empfangen.", get_user_log_info(update))
    help_text = "🤖 *Flipper Zero Release Bot*\n\n/momentum\n/unleashed\n/arf\n/protopirate\n/uptime\n/hilfe"
    await update.effective_message.reply_text(help_text, parse_mode=constants.ParseMode.MARKDOWN, link_preview_options=LinkPreviewOptions(is_disabled=True))

if __name__ == '__main__':
    if not TOKEN: exit(1)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_error_handler(error_handler)
    app.add_handler(CommandHandler("momentum", momentum))
    app.add_handler(CommandHandler("unleashed", unleashed))
    app.add_handler(CommandHandler("arf", arf))
    app.add_handler(CommandHandler("protopirate", protopirate))
    app.add_handler(CommandHandler("uptime", uptime))
    app.add_handler(CommandHandler("hilfe", hilfe))
    logger.info("Bot v1.4.9 gestartet.")
    app.run_polling()
