import random
from telegram import Update
from telegram.ext import ContextTypes

TRUTHS = [
    "Apni crush ka naam batao 😏",
    "Pehli love story kab start hui thi?",
    "Kisi se secret crush hai?"
]

DARES = [
    "Apne partner ko ❤️ bhejo",
    "Group me 'I am in love' likho",
    "Apni DP change karo 😜"
]

async def couplegame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Couple Games\n"
        "/truth – Truth question\n"
        "/dare – Dare challenge\n"
        "/lovepercent @user – Love meter ❤️"
    )

async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💬 Truth:\n" + random.choice(TRUTHS)
    )

async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Dare:\n" + random.choice(DARES)
    )

async def lovepercent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /lovepercent @username")
        return

    percent = random.randint(40, 100)
    await update.message.reply_text(
        f"❤️ Love Meter\n"
        f"You + {context.args[0]} = {percent}% 💕"
    )
