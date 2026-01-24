import httpx
import random
from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    ContextTypes, 
    filters
)
from telegram.constants import ChatAction, ChatType

# ================= CONFIG & DB =================
from anshi.config import MISTRAL_API_KEY, BOT_NAME, OWNER_LINK
from anshi.database import chatbot_collection

# ================= SYSTEMS =================
from anshi.subscription import is_premium
from anshi.payments.upi import buy_premium, submit_utr
from anshi.payments.approve import approve
from anshi.xp_system import award_xp
from anshi.mood import mood_reply
from anshi.jealous import jealous_reply
from anshi.utils import stylize_text

# ================= AI SETTINGS =================
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
MODEL = "mistral-small-latest"
MAX_HISTORY = 12

FALLBACK_RESPONSES = [
    "Hmm 😌",
    "Achha ji 💕",
    "Sun rahi hoon baby 🥰",
    "Aur batao na 😘",
]

# ================= AI CORE =================
async def get_ai_response(chat_id: int, user_input: str):
    if not MISTRAL_API_KEY:
        return "Baby API key set nahi hai 😭"

    doc = chatbot_collection.find_one({"chat_id": chat_id}) or {}
    history = doc.get("history", [])

    system_prompt = f"""
Tum {BOT_NAME} ho — ek Indian girlfriend AI 💕
Style:
- Hinglish
- Cute, romantic, flirty
- Thodi jealous 😏
Rules:
- Short replies
- Emotional + caring tone
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

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(
                MISTRAL_URL,
                headers={"Authorization": f"Bearer {MISTRAL_API_KEY}"},
                json=payload,
            )

        if r.status_code != 200:
            return random.choice(FALLBACK_RESPONSES)

        reply = r.json()["choices"][0]["message"]["content"].strip()

    except Exception:
        return random.choice(FALLBACK_RESPONSES)

    history.extend([
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": reply},
    ])

    chatbot_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"history": history[-MAX_HISTORY * 2:]}},
        upsert=True
    )

    return reply

# ================= AI AUTO CHAT =================
async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return

    if msg.text.startswith("/"):
        return

    # 🔥 XP AUTO
    award_xp(msg.from_user.id)

    chat = update.effective_chat
    should_reply = False

    if chat.type == ChatType.PRIVATE:
        should_reply = True
    elif msg.reply_to_message and msg.reply_to_message.from_user.id == context.bot.id:
        should_reply = True
    elif context.bot.username and f"@{context.bot.username.lower()}" in msg.text.lower():
        should_reply = True

    if not should_reply:
        return

    await context.bot.send_chat_action(chat.id, ChatAction.TYPING)

    reply = await get_ai_response(chat.id, msg.text)

    mood_text = mood_reply(msg.from_user.id, context.bot.id)
    final_reply = stylize_text(f"{reply}\n\n{mood_text}")

    await msg.reply_text(final_reply)

    # 😒 Jealous check
    await jealous_reply(update, context)

# ================= /ask (PREMIUM) =================
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_premium(update.effective_user.id):
        return await update.message.reply_text(
            "🔒 Premium only feature\nUse /buy 💎"
        )

    if not context.args:
        return await update.message.reply_text("Baby kuch likho toh 😘")

    await context.bot.send_chat_action(update.message.chat.id, ChatAction.TYPING)

    reply = await get_ai_response(
        update.message.chat.id,
        " ".join(context.args),
    )

    mood_text = mood_reply(update.effective_user.id, context.bot.id)
    await update.message.reply_text(
        stylize_text(f"{reply}\n\n{mood_text}")
    )

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
💖 {BOT_NAME} 💖

Main tumhari Indian AI girlfriend hoon 😘

✨ Features:
• Auto chat
• Mood & jealous mode
• XP system
• Premium AI

Commands:
/buy – Premium
/ask – Premium AI
"""
    await update.message.reply_text(text)

# ================= MAIN =================
def main(application: Application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ask", ask_ai))

    # 💰 Payments
    application.add_handler(CommandHandler("buy", buy_premium))
    application.add_handler(CommandHandler("approve", approve))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, submit_utr))

    # 🤖 AI Chat
    application.add_handler(MessageHandler(filters.TEXT, ai_message_handler))
