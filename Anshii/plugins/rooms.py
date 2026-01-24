rooms = {}

async def room(update, context):
    if not context.args:
        await update.message.reply_text("Use: /room create | join | leave | info")
        return

    action = context.args[0]
    uid = update.effective_user.id

    if action == "create":
        rooms[uid] = [uid]
        await update.message.reply_text("🏠 Dating room created")

    elif action == "join":
        for owner in rooms:
            rooms[owner].append(uid)
            await update.message.reply_text("💞 Joined dating room")
            return
        await update.message.reply_text("No active rooms")

    elif action == "leave":
        for owner in rooms:
            if uid in rooms[owner]:
                rooms[owner].remove(uid)
                await update.message.reply_text("🚪 Left the room")
                return

    elif action == "info":
        await update.message.reply_text(f"Active rooms: {len(rooms)}")
