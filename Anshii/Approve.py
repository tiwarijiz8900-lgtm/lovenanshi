from telegram import Update
from telegram.ext import ContextTypes
from anshi.subscription import activate_premium
from anshi.config import OWNER_ID

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    try:
        user_id = int(context.args[0])
        plan = context.args[1]  # monthly / yearly
    except:
        await update.message.reply_text(
            "❌ Usage:\n/approve user_id monthly|yearly"
        )
        return

    expiry = activate_premium(user_id, plan)

    if not expiry:
        await update.message.reply_text("❌ Invalid plan")
        return

    await update.message.reply_text(
        f"✅ Premium activated!\nUser: `{user_id}`\nPlan: {plan}\nExpiry: {expiry}",
        parse_mode="Markdown"
    )

    await context.bot.send_message(
        chat_id=user_id,
        text=f"🎉 Premium Activated!\nPlan: {plan}\nValid till: {expiry.date()} 💖"
    )
