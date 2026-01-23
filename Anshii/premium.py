from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from baka.database import subscription_collection

async def my_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    sub = subscription_collection.find_one({"user_id": user.id})

    if not sub:
        return await update.message.reply_text(
            "😅 Tum free user ho jaan\n\n"
            "💎 Premium le lo:\n"
            "➤ 2× XP\n"
            "➤ Faster ranking\n"
            "➤ Special love 💕"
        )

    await update.message.reply_text(
        f"💎 <b>Your Subscription</b>\n\n"
        f"Plan: <b>{sub['plan'].title()}</b>\n"
        f"XP Boost: <b>{sub['xp_boost']}×</b>\n\n"
        f"🔥 Grind faster, jaan!",
        parse_mode=ParseMode.HTML
    )
