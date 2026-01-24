from telegram import Update
from telegram.ext import ContextTypes

jealous_users = set()

async def jealous_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if not context.args:
        return await update.message.reply_text("Use: /jealous on | off")

    if context.args[0].lower() == "on":
        jealous_users.add(uid)
        await update.message.reply_text("😤 Jealous mode ON\nSirf meri baat suno 😒")
    else:
        jealous_users.discard(uid)
        await update.message.reply_text("🙂 Jealous mode OFF")

async def jealous_react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in jealous_users:
        await update.message.reply_text("😠 Tum kisi aur se baat kar rahe ho?")
