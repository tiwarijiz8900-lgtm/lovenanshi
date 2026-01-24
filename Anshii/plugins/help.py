from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

# ================= MAIN /help =================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💖 Love & Relationship", callback_data="help_love")],
        [InlineKeyboardButton("🎮 Games & Battles", callback_data="help_games")],
        [InlineKeyboardButton("🧠 AI & Chat", callback_data="help_ai")],
        [InlineKeyboardButton("💎 Premium & UPI", callback_data="help_premium")],
        [InlineKeyboardButton("🏆 XP & Leaderboard", callback_data="help_xp")],
        [InlineKeyboardButton("👮 Admin", callback_data="help_admin")],
    ]

    await update.message.reply_text(
        "📖 **Help Menu**\n\nCategory choose karo 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ================= CALLBACK HANDLER =================
async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    data = q.data

    if data == "help_love":
        text = (
            "💖 **LOVE & RELATIONSHIP**\n\n"
            "/propose – 💍 Propose user\n"
            "/marry – 💞 Relationship status\n"
            "/divorce – 💔 Breakup\n"
            "/couple – 💘 Couple game\n"
            "/wpropose – 💍 Waifu propose\n"
            "/wmarry – 💒 Random waifu\n"
            "Auto marriage, jealous mode, mood system enabled 💕"
        )

    elif data == "help_games":
        text = (
            "🎮 **GAMES & BATTLES**\n\n"
            "/kill – 🔪 Kill for coins\n"
            "/rob – 💰 Rob users\n"
            "/dice – 🎲 Gamble\n"
            "/slots – 🎰 Slot game\n"
            "/battle – ⚔️ Couple battle (Premium)\n"
            "/revive – ✨ Revive\n"
            "/protect – 🛡️ Protection"
        )

    elif data == "help_ai":
        text = (
            "🧠 **AI & CHAT**\n\n"
            "/chatbot – 🤖 AI settings\n"
            "/ask – 💬 Ask AI\n"
            "Mention bot or reply to chat 💕\n"
            "Indian girlfriend style enabled 🇮🇳"
        )

    elif data == "help_premium":
        text = (
            "💎 **PREMIUM & PAYMENT**\n\n"
            "/buy – 💳 Buy premium\n"
            "Monthly / Yearly plans\n"
            "Premium unlocks:\n"
            "• Dating rooms\n"
            "• Couple battles\n"
            "• Unlimited AI\n"
            "• Memory boost\n"
        )

    elif data == "help_xp":
        text = (
            "🏆 **XP & LEADERBOARD**\n\n"
            "/bal – 👛 Wallet & XP\n"
            "/ranking – 🏆 Leaderboard\n"
            "XP auto milta hai chats se 🔥"
        )

    elif data == "help_admin":
        text = (
            "👮 **ADMIN COMMANDS**\n\n"
            "/approve user_id plan – ✅ Approve premium\n"
            "/broadcast – 📢 Message all\n"
            "/addcoins – ➕ Add coins\n"
            "/rmcoins – ➖ Remove coins\n"
            "/update – 🔄 Restart bot"
        )

    else:
        text = "❌ Unknown help section"

    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="help_back")]]

    await q.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ================= BACK BUTTON =================
async def help_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await help_command(update, context)

    text = """
💖 *Anshika AI – Command List*

🌸 *Basic*
/start – Bot start
/help – All commands
/profile – Your profile

💞 *Love & Relationship*
/love – Love talk
/marry – Auto proposal
/breakup – Breakup mode
/jealous – Jealous mode
/relationship – Relationship status

🎮 *Games*
/couplegame – Couple game
/battle – Couple battle (VS system)

🏠 *Dating*
/room – Create dating room
/leaveroom – Leave room

⭐ *XP System*
/xp – Your XP
/leaderboard – Top lovers

💎 *Premium*
/buy – Buy premium
/plan – My plan

🌙 *Wishes*
/gm /gn /ge – Wishes

🇮🇳 Indian Girlfriend Mode
Auto flirting enabled ❤️
"""

    buttons = [
        [
            InlineKeyboardButton("💎 Buy Premium", callback_data="buy_premium"),
            InlineKeyboardButton("⭐ My XP", callback_data="my_xp")
        ],
        [
            InlineKeyboardButton("🏆 Leaderboard", callback_data="leaderboard"),
            InlineKeyboardButton("❤️ Relationship", callback_data="relationship")
        ]
    ]

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
