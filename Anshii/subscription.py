from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes

from Anshi.database import subscription_collection

# ===============================
# 💎 PLANS
# ===============================
PLANS = {
    "silver": {"days": 30, "price": 199},
    "gold": {"days": 90, "price": 499},
    "lifetime": {"days": 3650, "price": 1999}
}

# ===============================
# ✅ CHECK PREMIUM
# ===============================
def is_premium(user_id: int) -> bool:
    sub = subscription_collection.find_one({"user_id": user_id})
    if not sub:
        return False
    if sub["expiry"] < datetime.utcnow():
        return False
    return True

# ===============================
# 🧾 MY PLAN
# ===============================
async def myplan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    sub = subscription_collection.find_one({"user_id": user_id})

    if not sub or sub["expiry"] < datetime.utcnow():
        return await update.message.reply_text(
            "❌ Tum free user ho\n💎 Premium le lo flirting ++ 😌"
        )

    exp = sub["expiry"].strftime("%d %b %Y")
    await update.message.reply_text(
        f"💎 <b>Premium Active</b>\n"
        f"Plan: {sub['plan']}\n"
        f"Expiry: {exp}",
        parse_mode="HTML"
    )

# ===============================
# 🛒 BUY PLAN (ADMIN CONFIRM)
# ===============================
def activate_premium(user_id: int, plan: str):
    days = PLANS[plan]["days"]
    expiry = datetime.utcnow() + timedelta(days=days)

    subscription_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "plan": plan,
                "expiry": expiry,
                "activated_at": datetime.utcnow()
            }
        },
        upsert=True
    )
