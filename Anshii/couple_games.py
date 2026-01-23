import random
from telegram import Update
from telegram.ext import ContextTypes

# 💕 Love Questions
LOVE_QUESTIONS = [
    "Tumhara sabse cute habit kya hai? 😘",
    "Agar hum date pe jayein toh kaha chaloge? 💕",
    "Tum mujhe ek word me kaise describe karoge? 😏",
    "Tum romantic ho ya naughty? 😈",
]

# 😈 Truth or Dare
TRUTHS = [
    "Last crush ka naam kya tha? 😜",
    "Kabhi kisi se secretly pyaar kiya hai? 😏",
]

DARES = [
    "Mujhe ek romantic line bolo 💕",
    "Apna cutest emoji bhejo 😘",
]

# ❤️ Love Score
def calculate_love_score(user1: int, user2: int) -> int:
    random.seed(user1 + user2)
    return random.randint(40, 100)

# ================= COMMANDS =================

# /lovequiz
async def love_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(LOVE_QUESTIONS)
    await update.message.reply_text(f"💖 *Love Quiz*\n\n{q}", parse_mode="Markdown")


# /truth
async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = random.choice(TRUTHS)
    await update.message.reply_text(f"😈 *Truth*\n\n{t}", parse_mode="Markdown")


# /dare
async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    d = random.choice(DARES)
    await update.message.reply_text(f"🔥 *Dare*\n\n{d}", parse_mode="Markdown")


# /lovescore
async def love_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text(
            "Kisi ko reply karke `/lovescore` use karo 💕",
            parse_mode="Markdown"
        )

    user1 = update.message.from_user
    user2 = update.message.reply_to_message.from_user

    score = calculate_love_score(user1.id, user2.id)

    await update.message.reply_text(
        f"❤️ *Love Score*\n\n"
        f"{user1.first_name} ❤️ {user2.first_name}\n"
        f"Compatibility: *{score}%* 😍",
        parse_mode="Markdown"
    )
