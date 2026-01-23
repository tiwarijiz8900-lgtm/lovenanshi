from telegram import Update
from telegram.ext import ContextTypes
from Anshi.config import UPI_ID, UPI_NAME, ADMIN_ID

pending_payments = {}

async def buy_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    msg = f"""
💎 *Premium Plan*

💰 Amount: ₹99  
📌 Pay via UPI

👉 UPI ID:
`{UPI_ID}`

📛 Name: {UPI_NAME}

Payment ke baad *UTR / Transaction ID* bhejo 👇
"""
    await update.message.reply_text(msg, parse_mode="Markdown")
    pending_payments[user.id] = True


async def submit_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id not in pending_payments:
        return

    utr = update.message.text

    admin_msg = f"""
🧾 *New Payment Request*

👤 User: {user.first_name}
🆔 User ID: `{user.id}`
💳 UTR: `{utr}`
"""
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_msg,
        parse_mode="Markdown"
    )

    await update.message.reply_text(
        "✅ Payment request sent!\nAdmin verify karega, thoda wait karo 💖"
    )

    del pending_payments[user.id]
