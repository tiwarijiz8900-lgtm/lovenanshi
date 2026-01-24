import random
from telegram import Update
from telegram.ext import ContextTypes

pending_battles = {}

async def battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /battle @username")
        return

    challenger = update.effective_user.id
    opponent = context.args[0]

    pending_battles[opponent] = challenger
    await update.message.reply_text(
        f"💥 Battle request sent to {opponent}\nUse /acceptbattle"
    )

async def acceptbattle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    if user not in pending_battles:
        await update.message.reply_text("No battle request 😅")
        return

    challenger = pending_battles.pop(user)
    winner = random.choice([challenger, update.effective_user.id])

    await update.message.reply_text(
        f"🔥 Couple Battle Finished!\n🏆 Winner: {winner}\n+20 XP"
    )

async def rejectbattle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    pending_battles.pop(user, None)
    await update.message.reply_text("❌ Battle rejected")
