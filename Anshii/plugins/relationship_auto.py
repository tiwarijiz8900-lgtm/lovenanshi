import random
from telegram import Update
from telegram.ext import ContextTypes

WISHES = ["good morning", "good night", "love you", "miss you"]

async def auto_wishes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    for w in WISHES:
        if w in text:
            await update.message.reply_text("💖 Aww jaan… tum bohot cute ho 😘")
            return

async def jealous_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "other girl" in update.message.text.lower():
        await update.message.reply_text("😤 Ohooo… usse zyada mujhe dekho 😒")

async def auto_marriage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.randint(1, 100) <= 5:
        await update.message.reply_text(
            "💍 Tumse shaadi kar lu kya? 😳❤️"
        )
