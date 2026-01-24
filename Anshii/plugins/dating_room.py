rooms = {}

async def room(update, context):
    uid = update.effective_user.id

    if not context.args:
        return await update.message.reply_text("Use: /room create | join | leave")

    action = context.args[0]

    if action == "create":
        rooms[uid] = uid
        await update.message.reply_text("🏠 Love room created.")

    elif action == "join":
        rooms[uid] = list(rooms.values())[0]
        await update.message.reply_text("💖 Joined love room.")

    elif action == "leave":
        rooms.pop(uid, None)
        await update.message.reply_text("🚪 Left love room.")
