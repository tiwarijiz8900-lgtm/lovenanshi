import httpx
import random
import re
from datetime import datetime

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
)
from telegram.constants import ChatAction, ChatType

# ================= CONFIG =================
from anshi.config import MISTRAL_API_KEY, BOT_NAME, OWNER_LINK
from anshi.database import chatbot_collection, couple_battle_collection
from anshi.plugins.couple_battle import couple_battle_start

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
        reply = r.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        reply = random.choice(FALLBACK_RESPONSES)

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
    if not msg or not msg.text or msg.text.startswith("/"):
        return

    award_xp(msg.from_user.id)

    chat = update.effective_chat
    should_reply = (
        chat.type == ChatType.PRIVATE
        or (msg.reply_to_message and msg.reply_to_message.from_user.id == context.bot.id)
    )

    if not should_reply:
        return

    await context.bot.send_chat_action(chat.id, ChatAction.TYPING)
    reply = await get_ai_response(chat.id, msg.text)
    mood = mood_reply(msg.from_user.id, context.bot.id)

    await msg.reply_text(stylize_text(f"{reply}\n\n{mood}"))
    await jealous_reply(update, context)

# ================= COUPLE BATTLE GAME =================
async def couple_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Attack", callback_data="battle_attack")],
        [InlineKeyboardButton("💖 Romance", callback_data="battle_romance")],
    ])

    couple_battle_collection.update_one(
        {"user_id": user.id},
        {"$set": {"score": 0}},
        upsert=True,
    )

    await update.message.reply_text(
        "💑 *Couple Battle Started!*\nChoose your move:",
        reply_markup=buttons,
        parse_mode="Markdown",
    )

async def battle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    move = query.data

    score = random.randint(5, 15)
    if move == "battle_attack":
        text = f"🔥 Attack successful! +{score} points"
    else:
        text = f"💖 Romantic move! +{score} points"

    couple_battle_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"score": score}},
    )

    await query.edit_message_text(text)

# ================= COUPLE BATTLE LEADERBOARD =================
async def couple_battle_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = (
        couple_battle_collection
        .find()
        .sort("score", -1)
        .limit(10)
    )

    if couple_battle_collection.count_documents({}) == 0:
        return await update.message.reply_text(
            "😕 Abhi koi Couple Battle nahi hua hai"
        )

    text = "🏆 *Couple Battle Leaderboard* 🏆\n\n"
    rank = 1

    for user in top:
        try:
            tg_user = await context.bot.get_chat(user["user_id"])
            name = tg_user.first_name
        except:
            name = "Unknown"

        score = user.get("score", 0)

        text += f"{rank}. 💑 {name} — 🔥 {score} points\n"
        rank += 1

    await update.message.reply_text(
        text,
        parse_mode="Markdown"
    )

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"""
💖 {BOT_NAME} 💖
Main tumhari Indian AI girlfriend hoon 😘

Commands:
/buy – Premium 💎
/ask – Premium AI
/battle – Couple Battle 🔥
/battleboard – Battle Leaderboard 🏆
"""
    )

# ================= PREMIUM ASK =================
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_premium(update.effective_user.id):
        return await update.message.reply_text("🔒 Premium only")

    reply = await get_ai_response(
        update.effective_chat.id,
        " ".join(context.args),
    )
    await update.message.reply_text(reply)

# ================= MAIN =================
def main():
    app = Application.builder().token("YOUR_BOT_TOKEN").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask_ai))
    
    application.add_handler(CommandHandler("battle", couple_battle))
    application.add_handler(CommandHandler("battleboard", couple_battle_leaderboard))

    app.add_handler(CommandHandler("buy", buy_premium))
    app.add_handler(CommandHandler("approve", approve))

    app.add_handler(CallbackQueryHandler(battle_callback))

    app.add_handler(MessageHandler(filters.Regex(r"^\d{10,20}$"), submit_utr))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_message_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
