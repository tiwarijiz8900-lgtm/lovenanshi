from anshi.xp_system import award_xp
import httpx
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatAction, ChatType
from telegram.error import BadRequest

from baka.config import MISTRAL_API_KEY, BOT_NAME, OWNER_LINK
from baka.database import (
    chatbot_collection,
    memory_collection,
    subscription_collection
)
from anshi.utils import stylize_text
from anshi.xp_system import award_xp   # ✅ XP SYSTEM

# ======================
# SETTINGS
# ======================
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
MODEL = "mistral-small-latest"
MAX_HISTORY = 12

# ======================
# STICKERS
# ======================
STICKER_PACKS = [
    "RandomByDarkzenitsu",
    "Null_x_sticker_2",
    "pack_73bc9_by_TgEmojis_bot",
    "animation_0_8_Cat",
    "vhelw_by_CalsiBot",
    "MySet199",
    "Quby741"
]

FALLBACK_RESPONSES = [
    "Achha ji? (⁠•⁠‿⁠•⁠)",
    "Hmm… aur batao?",
    "Okk okk 😌",
    "Sahi hai yaar ✨",
    "Aur kya chal raha?",
    "Sunao sunao 💕"
]

# ======================
# STICKER HELPER
# ======================
async def send_ai_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pack = random.choice(STICKER_PACKS)
        sticker_set = await context.bot.get_sticker_set(pack)
        if sticker_set.stickers:
            await update.message.reply_sticker(
                random.choice(sticker_set.stickers).file_id
            )
            return True
    except:
        pass
    return False

# ======================
# AI CORE
# ======================
async def get_ai_response(chat_id: int, user_input: str, user_name: str):

    # 🔐 Save MEMORY (basic)
    memory_collection.update_one(
        {"user_id": chat_id},
        {"$set": {"last_message": user_input}},
        upsert=True
    )

    # 🧾 Load chat history
    doc = chatbot_collection.find_one({"chat_id": chat_id}) or {}
    history = doc.get("history", [])

    system_prompt = (
        f"Tum {BOT_NAME} ho — ek cute Indian girlfriend jo Hinglish me baat karti hai.\n"
        "Rules:\n"
        "- Short replies\n"
        "- No repetition\n"
        "- Cute + flirty + emotional\n"
        "- Natural girlfriend vibe\n"
        f"Owner: {OWNER_LINK}"
    )

    messages = [{"role": "system", "content": system_prompt}]
    for m in history[-MAX_HISTORY:]:
        messages.append(m)
    messages.append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.85,
        "max_tokens": 120
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(MISTRAL_URL, json=payload, headers=headers)
            if r.status_code != 200:
                return random.choice(FALLBACK_RESPONSES)

            reply = r.json()["choices"][0]["message"]["content"].strip()

            # Loop prevention
            if reply.lower() in [h["content"].lower() for h in history if h["role"] == "assistant"]:
                reply = random.choice(FALLBACK_RESPONSES)

            new_history = history + [
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": reply}
            ]
            chatbot_collection.update_one(
                {"chat_id": chat_id},
                {"$set": {"history": new_history[-MAX_HISTORY*2:]}},
                upsert=True
            )

            return reply

    except Exception as e:
        print(e)
        return "Net thoda slow hai baby 😅"

# ======================
# MESSAGE HANDLER
# ======================
async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.from_user:
        return

    chat = update.effective_chat

    # 🎮 XP AWARD
    award_xp(msg.from_user.id)

    # 💎 Subscription check (future use)
    is_premium = bool(
        subscription_collection.find_one({"user_id": msg.from_user.id})
    )

    # Stickers
    if msg.sticker:
        if chat.type == ChatType.PRIVATE:
            await send_ai_sticker(update, context)
        return

    if not msg.text or msg.text.startswith("/"):
        return

    text = msg.text.strip()
    should_reply = False

    if chat.type == ChatType.PRIVATE:
        should_reply = True
    else:
        cfg = chatbot_collection.find_one({"chat_id": chat.id}) or {}
        if not cfg.get("enabled", True):
            return

        botname = context.bot.username.lower()
        if msg.reply_to_message and msg.reply_to_message.from_user.id == context.bot.id:
            should_reply = True
        elif f"@{botname}" in text.lower():
            should_reply = True
            text = text.replace(f"@{botname}", "")
        elif text.lower().startswith(("hi", "hey", "baby", "babu", "jaan")):
            should_reply = True

    if not should_reply:
        return

    await context.bot.send_chat_action(chat.id, ChatAction.TYPING)
    reply = await get_ai_response(chat.id, text, msg.from_user.first_name)
    await msg.reply_text(stylize_text(reply))

    if random.random() < 0.3:
        await send_ai_sticker(update, context)

# ======================
# /ask COMMAND
# ======================
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text(
            "Use: /ask tum kya kar rahi ho?"
        )

    await context.bot.send_chat_action(
        update.message.chat.id,
        ChatAction.TYPING
    )

    reply = await get_ai_response(
        update.message.chat.id,
        " ".join(context.args),
        update.effective_user.first_name
    )
    await update.message.reply_text(stylize_text(reply))
