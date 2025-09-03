from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from dotenv import load_dotenv
from actions.actions import make_request, explore, take, insert, get_data

import sys
import os

load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ENV = os.getenv('ENVIRONMENT')

if not BOT_TOKEN or not WEBHOOK_URL:
    print("Error: BOT_TOKEN o WEBHOOK_URL not setted")
    sys.exit(0)

class Command:
    def __init__(self, cmd):
        self.cmd = cmd
        self.root = cmd[0][1:]
        self.options = None
        self.message = ''

    def set(self):
        if self.root == 'cal':
            if len(self.cmd) > 1:
                self.action = self.cmd[1]
                if len(self.cmd) > 2:
                    self.options = self.cmd[2:]
            else:
                self.message = 'few args'

    def execute(self):
        if self.root == 'cal':
            if self.action == 'req':
                res, msg = make_request()
                self.message = msg
            elif self.action == 'time':
                self.message = 'requesting time'
            elif self.action == 'act':
                msg = explore('act')
                self.message = msg
            elif self.action == 'end':
                msg = explore('end')
                self.message = msg
            elif self.action == 'ch':
                msg = explore('state')
                self.message = msg
            elif self.action == 'cols':
                msg = get_data('cols')
                self.message = msg
            else:
                self.message = 'not recognized action'
        else:
            self.message = 'not recognized cmd'

async def handle_document(update: Update, context):
    trans = take('transfer')
    if trans == True and update.message.document:
        doc = update.message.document
        if doc.mime_type == 'text/csv':
            file = await context.bot.get_file(doc.file_id)
            filepath = f'{doc.file_name}'
            insert('file', filepath)
            await file.download_to_drive(filepath)
        await update.message.reply_text("file uploaded")
    

async def caller(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    string = update.message.text.split(" ")
    cmd = Command(string)
    cmd.set()
    cmd.execute()

    await update.message.reply_text(f'{cmd.message}')

app = ApplicationBuilder().token(BOT_TOKEN).build()

cal_handler = CommandHandler('cal', caller)
doc_handler = MessageHandler(filters.Document.ALL, handle_document)

app.add_handler(cal_handler)
app.add_handler(doc_handler)

if ENV == 'development':
    app.run_polling()
elif ENV == 'production':
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        url_path=BOT_TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}",
    )
else:
    print('ENVIRONMENT is not recognized')


