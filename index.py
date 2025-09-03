from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from dotenv import load_dotenv
from actions.actions import make_request, explore, take_from_mani

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
                msg = explore('def')
                self.message = msg
            elif self.action == 'ch':
                msg = explore('state')
                self.message = msg
            else:
                self.message = 'not recognized action'
        else:
            self.message = 'not recognized cmd'

async def switch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    trans = take_from_mani('transfer')
    if trans == True:
        if update.message.document:
            doc = update.message.document
            if "mime_type" in doc:
                if doc.mime_type == 'text/csv':
                    file = await context.bot.get_file(doc.file_id)
                    file_path = f'{doc.file_name}'
                    await file.download_to_drive(file_path)
                print('transference done')

    string_cmd = update.message.text.split(" ")
    cmd = Command(string_cmd)
    cmd.set()
    cmd.execute()

    await update.message.reply_text(f'{cmd.message}')

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler('cal', switch))

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


