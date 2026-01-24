import random
from telegram import Update
from telegram.ext import ContextTypes
from baka.plugins.subscription import is_premium
from anshi.xp_system import award_xp

WIN_LINES = [
    "💞 Power couple nikle tum dono!",
    "🔥 Love + Power = Win!",
    "😍 Made for each other!",
]

LOSE_LINES = [
    "😅 Haar gaye, par pyaar zinda hai",
    "💔 Power kam pad gaya",
    "😌 Next round jeetoge pakka",
]

async def couple_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # 🔒 PREMIUM CHECK
    if not is_premium(user.id):
        return await update.message.reply_text(
            "🔒 Premium Couple Battle\nUse /buy 💎"
        )

    if not update.message.reply_to_message:
        return await update.message.reply_text(
            "👩‍❤️‍👨 Kisi couple ke message pe reply karke /cb likho"
        )

    opponent = update.message.reply_to_message.from_user

    if opponent.id == user.id:
        return await update.message.reply_text("😂 Khud se battle nahi hoti baby")

    your_power = random.randint(50, 120)
    enemy_power = random.randint(50, 120)

    text = (
        "⚔️ **COUPLE BATTLE** ⚔️\n\n"
        f"💑 {user.first_name} & ❤️ Partner\n"
        f"Power: {your_power}\n\n"
        f"💑 {opponent.first_name} & ❤️ Partner\n"
        f"Power: {enemy_power}\n\n"
    )

    if your_power > enemy_power:
        award_xp(user.id)
        award_xp(opponent.id)
        text += f"🏆 **YOU WON!**\n{random.choice(WIN_LINES)}\n✨ +XP"
    elif your_power < enemy_power:
        text += f"💔 **YOU LOST**\n{random.choice(LOSE_LINES)}"
    else:
        text += "😲 **DRAW!** Dono equal nikle"

    await update.message.reply_text(text, parse_mode="Markdown")
