from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from dotenv import load_dotenv
from command import Command

import sys
import os

load_dotenv()
BOT_TOKEN   = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ENV         = os.getenv('ENVIRONMENT')

if not BOT_TOKEN or not WEBHOOK_URL:
    print("Error: BOT_TOKEN o WEBHOOK_URL not setted")
    sys.exit(0)

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


