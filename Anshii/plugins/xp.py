xp_db = {}

async def add_xp(user_id, amount=1):
    xp_db[user_id] = xp_db.get(user_id, 0) + amount

async def xp(update, context):
    uid = update.effective_user.id
    await update.message.reply_text(f"⭐ Your XP: {xp_db.get(uid,0)}")

async def leaderboard(update, context):
    top = sorted(xp_db.items(), key=lambda x: x[1], reverse=True)[:5]
    msg = "🏆 XP Leaderboard\n"
    for i,(u,x) in enumerate(top,1):
        msg += f"{i}. {u} → {x} XP\n"
    await update.message.reply_text(msg)
