from telegram import Update
from telegram.ext import ContextTypes
from baka.plugins.subscription import activate_premium
from baka.config import OWNER_ID

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if len(context.args) != 2:
        return await update.message.reply_text(
            "Use: /approve user_id monthly|yearly"
        )

    user_id = int(context.args[0])
    plan = context.args[1]

    expiry = activate_premium(user_id, plan)
    if not expiry:
        return await update.message.reply_text("❌ Invalid plan")

    await update.message.reply_text(
        f"✅ Premium activated\n"
        f"👤 User: `{user_id}`\n"
        f"📅 Till: `{expiry.date()}`",
        parse_mode="Markdown"
    )
