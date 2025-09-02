from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import sys
import os

BOT_TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

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
        print('setting')
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
                self.message = 'making a request'
            else:
                self.message = 'not recognized action'
        else:
            self.message = 'not recognized cmd'

async def switch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    string_cmd = update.message.text.split(" ")
    cmd = Command(string_cmd)
    cmd.set()
    cmd.execute()

    await update.message.reply_text(f'{cmd.message}')

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler('cal', switch))
#app.run_polling()

app.run_webhook(
    listen="0.0.0.0",
    port=int(os.getenv("PORT", "5000")),
    url_path=BOT_TOKEN,
    webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}",
)

if __name__ == "__main__":
    main()

