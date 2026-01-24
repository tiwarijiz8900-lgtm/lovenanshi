from telegram import Update
from telegram.ext import ContextTypes
from anshi.database import xp_collection

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    # 🔝 Top 10 users by XP
    top_users = xp_collection.find().sort("xp", -1).limit(10)

    if xp_collection.count_documents({}) == 0:
        return await update.message.reply_text(
            "😅 Abhi koi XP data nahi hai\nChat karo pehle!"
        )

    text = "🏆 **XP LEADERBOARD** 🏆\n\n"

    rank = 1
    for user in top_users:
        name = user.get("name", "Unknown")
        xp = user.get("xp", 0)
        level = user.get("level", 1)

        text += (
            f"**{rank}. {name}**\n"
            f"✨ XP: `{xp}` | 🎚️ Level: `{level}`\n\n"
        )
        rank += 1

    await update.message.reply_text(text, parse_mode="Markdown")
