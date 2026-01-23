from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from baka.database import xp_collection
from baka.utils import get_mention

# =========================
# 🧮 USER XP & RANK
# =========================

async def my_xp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    data = xp_collection.find_one({"user_id": user.id})
    xp = data.get("xp", 0) if data else 0

    rank = xp_collection.count_documents({"xp": {"$gt": xp}}) + 1

    await update.message.reply_text(
        f"✨ <b>Your XP Stats</b> ✨\n\n"
        f"👤 {get_mention(user)}\n"
        f"⚡ XP: <b>{xp}</b>\n"
        f"🏆 Rank: <b>#{rank}</b>",
        parse_mode=ParseMode.HTML,
    )

# =========================
# 🏆 LEADERBOARD
# =========================

async def xp_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = xp_collection.find().sort("xp", -1).limit(10)

    if xp_collection.count_documents({}) == 0:
        return await update.message.reply_text("Abhi koi leaderboard nahi hai 😅")

    text = "🏆 <b>XP Leaderboard</b> 🏆\n\n"

    for i, user in enumerate(top, start=1):
        text += f"{i}. <code>{user['user_id']}</code> — ⚡ {user['xp']}\n"

    await update.message.reply_text(text, parse_mode=ParseMode.HTML)
