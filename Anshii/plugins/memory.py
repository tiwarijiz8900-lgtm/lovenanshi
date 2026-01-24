from telegram import Update
from telegram.ext import ContextTypes
from baka.database import memory_collection

async def save_memory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    memory_collection.insert_one({
        "user": update.effective_user.id,
        "text": update.message.text
    })

async def show_memory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = memory_collection.find(
        {"user": update.effective_user.id}
    ).limit(5)

    msg = "🧠 Your Memories:\n\n"
    for d in data:
        msg += f"• {d['text']}\n"

    await update.message.reply_text(msg)
