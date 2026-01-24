from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from baka.database import subscription_collection
from baka.config import OWNER_ID

PLANS = {
    "monthly": 30,
    "yearly": 365
}

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💎 Premium Plans\n\n"
        "• Monthly – ₹99\n"
        "• Yearly – ₹999\n\n"
        "Pay via UPI & send UTR to admin."
    )

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    try:
        user_id = int(context.args[0])
        plan = context.args[1]
        days = PLANS[plan]

        expiry = datetime.utcnow() + timedelta(days=days)

        subscription_collection.update_one(
            {"user_id": user_id},
            {"$set": {
                "user_id": user_id,
                "plan": plan,
                "expiry": expiry
            }},
            upsert=True
        )

        await update.message.reply_text(
            f"✅ Premium activated\nUser: `{user_id}`\nPlan: `{plan}`",
            parse_mode="Markdown"
        )
    except:
        await update.message.reply_text("❌ Usage: /approve user_id monthly|yearly")

async def myplan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = subscription_collection.find_one({"user_id": update.effective_user.id})
    if not data:
        await update.message.reply_text("❌ You are not premium")
    else:
        await update.message.reply_text(
            f"💎 Premium Active\nPlan: {data['plan']}\nExpiry: {data['expiry']}"
        )
