from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
