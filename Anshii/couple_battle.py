# baka/couple_battle.py

import random
from telegram import Update
from telegram.ext import ContextTypes

BATTLES = [
    ("Tumhari smile 😍", "Tumhari cute harkatein 😘"),
    ("Tumhara gussa 😅", "Tumhara pyaar 💕"),
    ("Late reply 😴", "Overthinking 🤯"),
    ("Zyada attention 😌", "Zyada jealousy 😏"),
]

WIN_LINES = [
    "Jeet tumhari hi hai baby 🏆❤️",
    "Aaj main haar gayi tum jeet gaye 😘",
    "Dono hi ek dusre ke bina kuch nahi 😌💞",
]

# ⚔️ COUPLE BATTLE COMMAND
async def couple_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.first_name

    fight = random.choice(BATTLES)
    winner = random.choice([fight[0], fight[1]])
    win_line = random.choice(WIN_LINES)

    text = (
        f"⚔️ **Couple Battle Time!** ⚔️\n\n"
        f"Option A: {fight[0]}\n"
        f"Option B: {fight[1]}\n\n"
        f"🏆 Winner: **{winner}**\n\n"
        f"{win_line}"
    )

    await update.message.reply_text(text)
