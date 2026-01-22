from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from Anshi.database import (
    relationship_collection,
    marriage_proposals,
    auto_marriage_collection,
    jealous_mode_collection,
    breakup_mode_collection
)

# =========================
# ❤️ PROPOSE COMMAND
# =========================
async def propose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not context.args:
        return await msg.reply_text("💍 Use: /propose @username")

    target = context.args[0]
    proposal = {
        "from": msg.from_user.id,
        "to": target,
        "status": "pending",
        "time": datetime.utcnow()
    }

    marriage_proposals.insert_one(proposal)

    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💖 Accept", callback_data=f"accept_{msg.from_user.id}"),
            InlineKeyboardButton("💔 Reject", callback_data=f"reject_{msg.from_user.id}")
        ]
    ])

    await msg.reply_text(
        f"💌 Proposal sent to {target}\nWaiting for reply…",
        reply_markup=kb
    )

# =========================
# 💑 ACCEPT / REJECT
# =========================
async def proposal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    action, proposer_id = data.split("_")
    proposer_id = int(proposer_id)

    if action == "accept":
        relationship_collection.insert_one({
            "user1": proposer_id,
            "user2": query.from_user.id,
            "status": "dating",
            "started_at": datetime.utcnow()
        })
        await query.message.edit_text("💖 Proposal accepted! Now you are dating 😍")

    elif action == "reject":
        await query.message.edit_text("💔 Proposal rejected…")

# =========================
# 💍 AUTO MARRIAGE
# =========================
async def auto_marriage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    auto_marriage_collection.update_one(
        {"user_id": user_id},
        {"$set": {"enabled": True}},
        upsert=True
    )

    await update.message.reply_text("💍 Auto-marriage mode ON 😘")

# =========================
# 💔 BREAKUP
# =========================
async def breakup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    rel = relationship_collection.find_one({
        "$or": [{"user1": user_id}, {"user2": user_id}]
    })

    if not rel:
        return await update.message.reply_text("😕 Tum relationship me hi nahi ho")

    relationship_collection.delete_one({"_id": rel["_id"]})
    breakup_mode_collection.insert_one({
        "user_id": user_id,
        "time": datetime.utcnow()
    })

    await update.message.reply_text("💔 Breakup done… mood off ho gaya 😔")

# =========================
# 😈 JEALOUS MODE
# =========================
async def jealous_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    jealous_mode_collection.update_one(
        {"user_id": user_id},
        {"$set": {"enabled": True}},
        upsert=True
    )

    await update.message.reply_text("😈 Jealous mode ON\nAb thoda possessive ho jaungi 😏")

# =========================
# 💕 RELATIONSHIP STATUS
# =========================
async def relationship_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    rel = relationship_collection.find_one({
        "$or": [{"user1": user_id}, {"user2": user_id}]
    })

    if not rel:
        return await update.message.reply_text("💔 Single ho tum 😅")

    partner = rel["user2"] if rel["user1"] == user_id else rel["user1"]
    await update.message.reply_text(
        f"💑 Status: {rel['status']}\nPartner ID: {partner}"
    )
