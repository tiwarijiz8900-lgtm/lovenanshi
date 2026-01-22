import httpx
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatAction, ChatType
from telegram.error import BadRequest

from baka.config import MISTRAL_API_KEY, BOT_NAME, OWNER_LINK
from baka.database import chatbot_collection
from baka.utils import stylize_text

# 🔥 XP SYSTEM IMPORT
from baka.xp_system import award_xp

# ================= SETTINGS =================
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
MODEL = "mistral-small-latest"
MAX_HISTORY = 12
# ===========================================


STICKER_PACKS = [
    "https://t.me/addstickers/RandomByDarkzenitsu",
    "https://t.me/addstickers/Null_x_sticker_2",
    "https://t.me/addstickers/animation_0_8_Cat",
]

FALLBACK_RESPONSES = [
    "Achha ji? (⁠•⁠‿⁠•⁠)",
    "Okk okk!",
    "Hmm… aur batao 💕",
    "Sunao na 😌",
]

# ================= AI CORE =================
async def get_ai_response(chat_id: int, user_input: str, user_name: str):
    if not MISTRAL_API_KEY:
        return "Baby API key missing hai 😭"

    doc = chatbot_collection.find_one({"chat_id": chat_id}) or {}
    history = doc.get("history", [])

    system_prompt = f"""
Tum {BOT_NAME} ho — ek **Indian girlfriend AI** 💕
Style:
- Full Hinglish
- Unlimited flirting 😘
- Cute + thoda jealous 😏
Rules:
- 1–2 lines max
- Natural girlfriend vibes
- Repeating sawal mat puchna
Owner: {OWNER_LINK}
"""

    messages = [{"role": "system", "content": system_prompt}]
    for h in history[-MAX_HISTORY:]:
        messages.append(h)
    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.85,
        "max_tokens": 120,
    }

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(
            MISTRAL_URL,
            headers={"Authorization": f"Bearer {MISTRAL_API_KEY}"},
            json=payload
        )
        if r.status_code != 200:
            return "Mood off hai baby 😅"

        reply = r.json()["choices"][0]["message"]["content"].strip()

    history += [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": reply},
    ]
    history = history[-MAX_HISTORY * 2:]

    chatbot_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"history": history}},
        upsert=True
    )

    return reply

# ================= MESSAGE HANDLER =================
async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    # 🔥 XP AUTO AWARD (YAHI ADD HUA HAI)
    if msg.from_user:
        award_xp(msg.from_user.id)

    chat = update.effective_chat

    if not msg.text or msg.text.startswith("/"):
        return

    should_reply = False

    if chat.type == ChatType.PRIVATE:
        should_reply = True
    else:
        doc = chatbot_collection.find_one({"chat_id": chat.id})
        if doc and not doc.get("enabled", True):
            return

        if msg.reply_to_message and msg.reply_to_message.from_user.id == context.bot.id:
            should_reply = True
        elif context.bot.username and f"@{context.bot.username.lower()}" in msg.text.lower():
            should_reply = True

    if not should_reply:
        return

    await context.bot.send_chat_action(chat.id, ChatAction.TYPING)

    reply = await get_ai_response(
        chat.id,
        msg.text,
        msg.from_user.first_name
    )

    await msg.reply_text(stylize_text(reply))

# ================= /ask COMMAND =================
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Baby kuch likho toh 😘")

    await context.bot.send_chat_action(update.message.chat.id, ChatAction.TYPING)
    reply = await get_ai_response(
        update.message.chat.id,
        " ".join(context.args),
        update.message.from_user.first_name
    )
    await update.message.reply_text(stylize_text(reply))
