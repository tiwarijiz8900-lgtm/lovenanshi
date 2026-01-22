from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from Anshi.subscription import PLANS

# ===============================
# 💸 UPI DETAILS
# ===============================
UPI_ID = "yourupi@paytm"
OWNER_ID = 123456789  # apna Telegram ID daalo

# ===============================
# 🛒 BUY COMMAND
# ===============================
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "💎 <b>Premium Plans</b>\n\n"
    kb = []

    for p, v in PLANS.items():
        text += f"• {p.title()} — ₹{v['price']}\n"
        kb.append([
            InlineKeyboardButton(
                f"Buy {p.title()}",
                callback_data=f"buy_{p}"
            )
        ])

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(kb)
    )

# ===============================
# 💳 PAYMENT CALLBACK
# ===============================
async def payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    plan = q.data.split("_")[1]

    amount = PLANS[plan]["price"]

    await q.message.edit_text(
        f"💸 <b>Payment</b>\n\n"
        f"Plan: {plan.title()}\n"
        f"Amount: ₹{amount}\n\n"
        f"📌 UPI ID:\n<code>{UPI_ID}</code>\n\n"
        f"Payment ke baad admin ko screenshot bhejo 👍",
        parse_mode="HTML"
    )
