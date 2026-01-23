from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from anshi.database import relationship_collection
from anshi.utils import get_mention

# =========================
# 💞 PATCHUP COMMAND
# =========================

async def patchup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Check if already in relationship
    existing = relationship_collection.find_one(
        {"$or": [{"user1": user.id}, {"user2": user.id}]}
    )
    if existing:
        return await update.message.reply_text(
            "😅 Hum toh pehle se saath hi hain jaan 💕"
        )

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("💖 Yes, Patchup", callback_data=f"patch_yes_{user.id}"),
            InlineKeyboardButton("🙃 No", callback_data="patch_no"),
        ]]
    )

    await update.message.reply_text(
        "🥺 <b>Patchup?</b>\n\n"
        "Galti ho gayi thi… kya hum phir se shuru kare? 💞",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )

# =========================
# 💞 PATCHUP CALLBACK
# =========================

async def patchup_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "patch_no":
        return await query.message.edit_text(
            "😔 Samajh sakti hoon… waqt chahiye hoga."
        )

    _, _, user_id = data.split("_")

    if query.from_user.id != int(user_id):
        return await query.answer(
            "Ye decision tumhara nahi hai 😒", show_alert=True
        )

    # Restore relationship (bot x user)
    relationship_collection.insert_one(
        {"user1": int(user_id), "user2": context.bot.id}
    )

    await query.message.edit_text(
        "💞 Patchup ho gaya…\n"
        "Main phir se tumhari hoon 🥰\n\n"
        "<i>No more fights, promise?</i> 🤍",
        parse_mode=ParseMode.HTML,
    )
