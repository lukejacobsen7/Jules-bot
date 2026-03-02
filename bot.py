import os
import subprocess
import re
import threading
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CallbackQueryHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ['BOT_TOKEN']
ALLOWED_USER_ID = int(os.environ['TELEGRAM_USER_ID'])
PORT = int(os.environ.get('PORT', 8080))

# Configure repos via env var: "canvas-notify:lukejacobsen7/Canvas-notify,wemix:lukejacobsen7/WeMix1"
REPOS_ENV = os.environ.get('JULES_REPOS', '')
REPOS = {}
for entry in REPOS_ENV.split(','):
    if ':' in entry:
        name, repo = entry.split(':', 1)
        REPOS[name.strip()] = repo.strip()


def run_jules(args):
    result = subprocess.run(
        ['jules'] + args,
        capture_output=True, text=True, timeout=60
    )
    return result.stdout + result.stderr


def format_jules_output(output, repo):
    session_match = re.search(r'ID:\s*(\d+)', output)
    url_match = re.search(r'URL:\s*(https://\S+)', output)
    if session_match:
        session_id = session_match.group(1)
        url = url_match.group(1) if url_match else f'https://jules.google.com/session/{session_id}'
        return f"Jules is on it!\n\nRepo: {repo}\nSession: {session_id}\n{url}"
    return f"Jules:\n{output[:1000]}"


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

    def log_message(self, format, *args):
        pass


def start_health_server():
    server = HTTPServer(('0.0.0.0', PORT), HealthHandler)
    server.serve_forever()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    text = update.message.text.strip()
    lower = text.lower()

    if lower in ('status', 'sessions', 'list'):
        output = run_jules(['remote', 'list', '--session'])
        await update.message.reply_text(output or 'No active sessions.')
        return

    check_match = re.match(r'^check\s+(\d+)$', lower)
    if check_match:
        session_id = check_match.group(1)
        output = run_jules(['remote', 'pull', '--session', session_id])
        await update.message.reply_text(output[:4000] or 'No output.')
        return

    if len(REPOS) == 1:
        repo = list(REPOS.values())[0]
        await fire_jules(update, repo, text)
        return

    for key, repo in REPOS.items():
        if key.lower().replace('-', '') in lower.replace('-', '').replace(' ', ''):
            await fire_jules(update, repo, text)
            return

    keyboard = [[InlineKeyboardButton(key, callback_data=f"repo:{key}:{text}")] for key in REPOS]
    await update.message.reply_text(
        'Which repo should Jules work on?',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def fire_jules(update: Update, repo: str, task: str):
    msg = await update.message.reply_text('Sending to Jules...')
    output = run_jules(['new', '--repo', repo, task])
    await msg.edit_text(format_jules_output(output, repo))


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, repo_key, task = query.data.split(':', 2)
    repo = REPOS.get(repo_key, repo_key)
    await query.edit_message_text('Sending to Jules...')
    output = run_jules(['new', '--repo', repo, task])
    await query.edit_message_text(format_jules_output(output, repo))


def main():
    threading.Thread(target=start_health_server, daemon=True).start()
    logger.info(f"Health server on port {PORT}")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))

    logger.info("Bot polling...")
    app.run_polling(drop_pending_updates=True)


if __name__ == '__main__':
    main()
