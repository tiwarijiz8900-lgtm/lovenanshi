from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from anshi.config import UPI_ID, UPI_NAME, MONTHLY_PRICE, YEARLY_PRICE, OWNER_ID
from anshi.database import pending_payments_collection
from anshi.subscription import activate_premium

# ================= /buy =================
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💎 **PREMIUM PLANS** 💎\n\n"
        f"📅 Monthly: ₹{MONTHLY_PRICE}\n"
        f"🗓️ Yearly: ₹{YEARLY_PRICE}\n\n"
        f"💳 **UPI ID:** `{UPI_ID}`\n"
        f"👤 Name: {UPI_NAME}\n\n"
        "✅ Payment ke baad **UTR number bhejo**\n"
        "Example: `123456789012`"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# ================= UTR HANDLER =================
async def submit_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text.isdigit():
        return

    utr = update.message.text
    user = update.effective_user

    pending_payments_collection.insert_one({
        "user_id": user.id,
        "name": user.first_name,
        "utr": utr,
        "date": datetime.utcnow()
    })

    await update.message.reply_text(
        "✅ UTR received!\nAdmin approve karte hi premium active ho jayega 💕"
    )

# ================= /approve =================
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("❌ Only owner can approve")

    if not context.args or len(context.args) < 2:
        return await update.message.reply_text(
            "Usage:\n/approve user_id monthly/yearly"
        )

    user_id = int(context.args[0])
    plan = context.args[1]

    expiry = activate_premium(user_id, plan)

    if not expiry:
        return await update.message.reply_text("❌ Invalid plan")

    pending_payments_collection.delete_one({"user_id": user_id})

    await update.message.reply_text(
        f"✅ Premium activated for `{user_id}`\n🗓️ Expiry: {expiry}",
        parse_mode="Markdown"
    )
