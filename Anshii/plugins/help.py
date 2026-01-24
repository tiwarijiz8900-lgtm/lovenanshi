from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def help_cmd(update, context):
    kb = [
        [InlineKeyboardButton("💖 Love", callback_data="h_love")],
        [InlineKeyboardButton("⚔️ Couple Battle", callback_data="h_battle")],
        [InlineKeyboardButton("🏠 Dating Room", callback_data="h_room")],
        [InlineKeyboardButton("🏆 XP", callback_data="h_xp")],
        [InlineKeyboardButton("💎 Premium", callback_data="h_premium")]
    ]
    await update.message.reply_text(
        "📖 Help Menu",
        reply_markup=InlineKeyboardMarkup(kb)
    )
