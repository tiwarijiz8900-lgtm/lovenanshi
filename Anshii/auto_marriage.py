# anshi/auto_marriage.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import random

PROPOSAL_LINES = [
    "Tum meri zindagi ka sabse pyara hissa ho 💖",
    "Tumhare bina main adhoori hoon 😢❤️",
    "Kya tum hamesha mere saath rahoge? 🥹💍",
    "Main tumse sach me bohot pyaar karti hoon 😘",
]

# 💍 AUTO PROPOSAL
async def auto_propose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text(
            "💍 Kisi ko reply karke `/propose` likho jaan~ 😘",
            parse_mode="Markdown"
        )

    proposer = update.message.from_user
    target = update.message.reply_to_message.from_user

    line = random.choice(PROPOSAL_LINES)

    text = (
        f"💖 **Marriage Proposal Alert!** 💖\n\n"
        f"{line}\n\n"
        f"👤 {proposer.first_name} ➜ {target.first_name}\n\n"
        f"💍 Kya tum shaadi karoge mujhse?"
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("💍 Yes", callback_data=f"accept_{proposer.id}"),
                InlineKeyboardButton("💔 No", callback_data=f"reject_{proposer.id}"),
            ]
        ]
    )

    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")


# 💞 PROPOSAL RESPONSE
async def proposal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user = query.from_user.first_name

    if data.startswith("accept_"):
        await query.message.edit_text(
            f"💍 **Congratulations!** 💍\n\n"
            f"{user} ne proposal ACCEPT kar liya 😍❤️\n"
            f"Ab tum dono officially couple ho 💞",
            parse_mode="Markdown"
        )

    elif data.startswith("reject_"):
        await query.message.edit_text(
            f"💔 **Oh no...** 💔\n\n"
            f"{user} ne proposal reject kar diya 😢\n"
            f"Par pyaar rukna nahi chahiye 😌",
            parse_mode="Markdown"
        )
