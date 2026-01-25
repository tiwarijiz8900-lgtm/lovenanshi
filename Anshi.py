import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"

from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ChatMemberHandler, filters
)
from telegram.request import HTTPXRequest

# ================= CONFIG =================
from anshi.config import TOKEN, PORT, BOT_NAME
from anshi.utils import log_to_channel

# ================= PLUGINS =================
from anshi.plugins import (
    start,
    help as help_plugin,
    subscription,
    leaderboard,
    battle,
    rooms,
    couple_games,
    wishes,
    jealous,
    memory,
)

from anshi.plugins.payments.upi import buy, submit_utr
from anshi.plugins.admin_premium import approve
from anshi.plugins.xp import add_xp
from anshi.plugins.chatbot import ai_message_handler

# ================= FLASK (HEROKU) =================
app = Flask(__name__)

@app.route("/")
def health():
    return "Alive"

def run_flask():
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

# ================= POST INIT =================
async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "🌸 Start"),
        ("help", "📖 Help Menu"),
        ("buy", "💳 Buy Premium"),
        ("myplan", "💎 My Subscription"),
        ("leaderboard", "🏆 XP Leaderboard"),
        ("battle", "⚔️ Couple Battle"),
        ("room", "🏠 Dating Room"),
        ("couplegame", "🎮 Couple Games"),
        ("gm", "☀️ Good Morning"),
        ("gn", "🌙 Good Night"),
    ])

    me = await application.bot.get_me()
    await log_to_channel(application.bot, "start", {
        "action": f"{BOT_NAME} (@{me.username}) started successfully 🚀"
    })

# ================= MAIN =================
if __name__ == "__main__":

    # ---- Flask Thread ----
    Thread(target=run_flask, daemon=True).start()

    if not TOKEN:
        raise SystemExit("❌ BOT TOKEN missing")

    request = HTTPXRequest(
        connection_pool_size=20,
        connect_timeout=60,
        read_timeout=60
    )

    app_bot = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(request)
        .post_init(post_init)
        .build()
    )

    # ================= BASIC =================
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("help", help_plugin.help_command))
    app_bot.add_handler(CallbackQueryHandler(help_plugin.help_callback, pattern="^help_"))

    # ================= PREMIUM / UPI =================
    app_bot.add_handler(CommandHandler("buy", buy))
    app_bot.add_handler(CommandHandler("approve", approve))
    app_bot.add_handler(CommandHandler("myplan", subscription.myplan))
    app_bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, submit_utr),
        group=1
    )

    # ================= XP =================
    app_bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, add_xp),
        group=2
    )

    # ================= LEADERBOARD =================
    app_bot.add_handler(CommandHandler("leaderboard", leaderboard.leaderboard))
    app_bot.add_handler(CommandHandler("top", leaderboard.leaderboard))

    # ================= COUPLE / GAMES =================
    app_bot.add_handler(CommandHandler("battle", battle.battle))
    app_bot.add_handler(CommandHandler("acceptbattle", battle.accept_battle))
    app_bot.add_handler(CommandHandler("room", rooms.room))

    app_bot.add_handler(CommandHandler("couplegame", couple_games.couplegame))
    app_bot.add_handler(CommandHandler("truth", couple_games.truth))
    app_bot.add_handler(CommandHandler("dare", couple_games.dare))
    app_bot.add_handler(CommandHandler("lovepercent", couple_games.lovepercent))

    # ================= WISHES =================
    app_bot.add_handler(CommandHandler("gm", wishes.gm))
    app_bot.add_handler(CommandHandler("gn", wishes.gn))
    app_bot.add_handler(CommandHandler("ge", wishes.ge))
    app_bot.add_handler(CommandHandler("love", wishes.love))
     
    # ================= MEMORY =================
    app_bot.add_handler(CommandHandler("memory", memory.show_memory))
    app_bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, memory.save_memory),
        group=3
    )

    # ================= JEALOUS MODE =================
    app_bot.add_handler(CommandHandler("jealous", jealous.jealous_cmd))
    app_bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, jealous.jealous_react),
        group=4
    )

    application.add_handler(CommandHandler("setname", setname))

    # ================= AI CHAT (LAST) =================
    app_bot.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, ai_message_handler),
        group=10
    )

    print("✅ LoveAnshi Bot running…")
    app_bot.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )
