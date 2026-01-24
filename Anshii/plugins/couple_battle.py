import random
from telegram import Update
from telegram.ext import ContextTypes

pending_battles = {}

async def battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Use: /battle @username")

    opponent = context.args[0]
    pending_battles[opponent] = update.effective_user.id

    await update.message.reply_text(
        f"💥 Battle request sent to {opponent}\nThey must use /acceptbattle"
    )

async def accept_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username not in pending_battles:
        return await update.message.reply_text("No battle request found.")

    challenger = pending_battles.pop(user.username)

    p1 = random.randint(1, 100)
    p2 = random.randint(1, 100)

    winner = "You ❤️" if p2 > p1 else "Opponent 😈"

    await update.message.reply_text(
        f"⚔️ Couple Battle Result ⚔️\n"
        f"You: {p2}\nOpponent: {p1}\n\n🏆 Winner: {winner}"
    )
