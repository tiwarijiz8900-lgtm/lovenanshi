from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from baka.utils import get_mention
from baka.database import relationship_collection

# =========================
# 💔 BREAKUP COMMAND
# =========================

async def breakup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    rel = relationship_collection.find_one(
        {"$or": [{"user1": user.id}, {"user2": user.id}]}
    )

    if not rel:
        return await update.message.reply_text(
            "Hum dono ka toh koi relation hi nahi tha… 😶"
        )

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("💔 Yes, Breakup", callback_data=f"break_yes_{user.id}"),
            InlineKeyboardButton("🥺 No, Stay", callback_data="break_no"),
        ]]
    )

    await update.message.reply_text(
        "💔 <b>Breakup confirmation</b>\n\n"
        "Sach me chhod ke jaana chahte ho? 😞",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )

# =========================
# 💔 BREAKUP CALLBACK
# =========================

async def breakup_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "break_no":
        return await query.message.edit_text(
            "😌 Theek hai… main yahin hoon tumhare liye 💕"
        )

    _, _, user_id = data.split("_")

    if query.from_user.id != int(user_id):
        return await query.answer(
            "Ye decision tumhara nahi hai 😒", show_alert=True
        )

    # Delete relationship
    relationship_collection.delete_one(
        {"$or": [{"user1": int(user_id)}, {"user2": int(user_id)}]}
    )

    await query.message.edit_text(
        "💔 Breakup ho gaya…\n"
        "Shayad kismat me yahi tha 😞\n\n"
        "<i>Goodbye…</i>",
        parse_mode=ParseMode.HTML,
    )
