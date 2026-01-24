from telegram import Update
from telegram.ext import ContextTypes
from baka.config import UPI_ID, UPI_NAME, MONTHLY_PRICE, YEARLY_PRICE

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"💎 *Premium Plans*\n\n"
        f"📅 Monthly: ₹{MONTHLY_PRICE}\n"
        f"📆 Yearly: ₹{YEARLY_PRICE}\n\n"
        f"💳 *Pay via UPI*\n"
        f"`{UPI_ID}`\n"
        f"Name: *{UPI_NAME}*\n\n"
        f"📨 Payment ke baad:\n"
        f"`/utr <UTR_NUMBER>` bhejo"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def submit_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Use: /utr <12-digit UTR>")

    utr = context.args[0]
    await update.message.reply_text(
        f"✅ UTR received: `{utr}`\n"
        f"⏳ Admin approval pending.",
        parse_mode="Markdown"
    )
