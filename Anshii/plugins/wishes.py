from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

async def gm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌞 Good Morning jaan ❤️")

async def gn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌙 Good Night sweet dreams 💕")

async def ge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌆 Good Evening cutie 😘")

async def love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❤️ I love you sooo much 😍")

async def auto_wishes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "good morning" in text:
        await update.message.reply_text("🌞 GM jaan 💖")
    elif "good night" in text:
        await update.message.reply_text("🌙 GN sweet dreams 😴")
    elif "good evening" in text:
        await update.message.reply_text("🌆 GE meri jaan 😘")
