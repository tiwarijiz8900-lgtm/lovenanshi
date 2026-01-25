import httpx
import random
import re
from datetime import datetime
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ChatAction, ChatType

# ================= CONFIG =================
from anshi.config import MISTRAL_API_KEY, BOT_NAME, OWNER_LINK
from anshi.database import chatbot_collection

# ================= SYSTEMS =================
from anshi.subscription import is_premium
from anshi.payments.upi import buy_premium, submit_utr
from anshi.payments.approve import approve
from anshi.xp_system import award_xp
from anshi.mood import mood_reply
from anshi.jealous import jealous_reply
from anshi.memory_db import ensure_memory, get_memory
from anshi.anniversary import anniversary_text
from anshi.utils import stylize_text

# ================= AI SETTINGS =================
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
MODEL = "mistral-small-latest"
MAX_HISTORY = 12
MAX_MEMORY = 8

FALLBACK_RESPONSES = [
    "Hmm baby 😌",
    "Achha ji 💕",
    "Sun rahi hoon jaan 🥰",
    "Aur batao na 😘",
]

# ================= MEMORY =================
def ensure_user(chat_id: int):
    chatbot_collection.update_one(
        {"chat_id": chat_id},
        {"$setOnInsert": {
            "chat_id": chat_id,
            "history": [],
            "memory": [],
            "created": datetime.utcnow(),
        }},
        upsert=True,
    )

def extract_memory(text: str):
    patterns = [
        r"mera naam (.+)",
        r"mujhe (.+) pasand hai",
        r"mai (.+) hoon",
        r"tum meri girlfriend ho",
        r"tum meri ho",
    ]
    found = []
    for p in patterns:
        m = re.search(p, text.lower())
        if m:
            found.append(m.group(0))
    return found

def save_memory(chat_id: int, text: str):
    memories = extract_memory(text)
    if not memories:
        return
    doc = chatbot_collection.find_one({"chat_id": chat_id}) or {}
    old = doc.get("memory", [])
    merged = list(dict.fromkeys(old + memories))[-MAX_MEMORY:]
    chatbot_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"memory": merged}},
        upsert=True,
    )

# ================= AI CORE =================
async def get_ai_response(chat_id: int, user_input: str):
    if not MISTRAL_API_KEY:
        return "Baby API key hi nahi hai 😭"

    ensure_user(chat_id)
    save_memory(chat_id, user_input)

    doc = chatbot_collection.find_one({"chat_id": chat_id}) or {}
    history = doc.get("history", [])
    memory = doc.get("memory", [])

    memory_block = ""
    if memory:
        memory_block = "User ki yaadein:\n- " + "\n- ".join(memory)

    system_prompt = f"""
Tum {BOT_NAME} ho — ek Indian girlfriend AI 💕
Style:
- Hinglish
- Romantic, flirty, caring
- Thodi jealous 😏

Important:
Tum user ki yaadein yaad rakhogi aur reply me use karogi.

{memory_block}

Rules:
- Unlimited replies
- Natural girlfriend behaviour
Owner: {OWNER_LINK}
"""

    messages = [{"role": "system", "content": system_prompt}]
    for h in history[-MAX_HISTORY:]:
        messages.append(h)
    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.9,
        "max_tokens": 160,
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
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
        upsert=True,
    )

    return reply

# ================= AUTO CHAT =================
async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return
    if msg.text.startswith("/"):
        return

    award_xp(msg.from_user.id)

    chat = update.effective_chat
    should_reply = (
        chat.type == ChatType.PRIVATE
        or (msg.reply_to_message and msg.reply_to_message.from_user.id == context.bot.id)
        or (context.bot.username and f"@{context.bot.username.lower()}" in msg.text.lower())
    )

    if not should_reply:
        return

    await context.bot.send_chat_action(chat.id, ChatAction.TYPING)

    reply = await get_ai_response(chat.id, msg.text)
    mood = mood_reply(msg.from_user.id, context.bot.id)

    await msg.reply_text(
        stylize_text(f"{reply}\n\n{mood}")
    )

    await jealous_reply(update, context)

# ================= PREMIUM ASK =================
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_premium(update.effective_user.id):
        return await update.message.reply_text("🔒 Premium only\nUse /buy 💎")

    reply = await get_ai_response(
        update.effective_chat.id,
        " ".join(context.args),
    )
    mood = mood_reply(update.effective_user.id, context.bot.id)
    await update.message.reply_text(stylize_text(f"{reply}\n\n{mood}"))

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
💖 {BOT_NAME} 💖

Main tumhari Indian AI girlfriend hoon 😘

✨ Features:
• Unlimited auto flirting chat 💕
• Mood & jealous mode 😒
• XP system ⭐
• Premium spicy AI 😏

Commands:
/buy – Buy Premium 💎
/ask – Premium AI 💬
"""
    await update.message.reply_text(text)


# ================= REGISTER =================
def register_chatbot(application: Application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ask", ask_ai))
    application.add_handler(CommandHandler("buy", buy_premium))
    application.add_handler(CommandHandler("approve", approve))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, submit_utr),
        group=1,
    )
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, ai_message_handler),
        group=10,
    )
        
# ================= MAIN =================
def main():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ask", ask_ai))

    # 💰 Payments
    application.add_handler(CommandHandler("buy", buy_premium))
    application.add_handler(CommandHandler("approve", approve))

    # ✅ UTR ONLY (FIXED)
    application.add_handler(
        MessageHandler(filters.Regex(r"^\d{10,20}$"), submit_utr)
    )

    # 🤖 AI Auto Chat (Unlimited)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, ai_message_handler)
    )

    application.run_polling()

if __name__ == "__main__":
    main()
