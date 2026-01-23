from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto,
)
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType

from baka.config import (
    BOT_NAME,
    START_IMG_URL,
    HELP_IMG_URL,
    SUPPORT_GROUP,
    SUPPORT_CHANNEL,
    OWNER_LINK,
)
from baka.utils import (
    ensure_user_exists,
    get_mention,
    track_group,
    log_to_channel,
    SUDO_USERS,
)

# =========================
# 🖼️ IMAGES
# =========================
SUDO_IMG = "https://files.catbox.moe/gyi5iu.jpg"

# =========================
# ⌨️ KEYBOARDS
# =========================

def get_start_keyboard(bot_username: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📢 Updates", url=SUPPORT_CHANNEL),
                InlineKeyboardButton("💬 Support", url=SUPPORT_GROUP),
            ],
            [
                InlineKeyboardButton(
                    "➕ Add Me To Group ➕",
                    url=f"https://t.me/{bot_username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton("📖 Help Menu", callback_data="help_main"),
                InlineKeyboardButton("👑 Owner", url=OWNER_LINK),
            ],
        ]
    )


def get_help_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("💍 Love", callback_data="help_social"),
                InlineKeyboardButton("💰 Economy", callback_data="help_economy"),
            ],
            [
                InlineKeyboardButton("⚔️ RPG", callback_data="help_rpg"),
                InlineKeyboardButton("🧠 AI & Fun", callback_data="help_fun"),
            ],
            [
                InlineKeyboardButton("⚙️ Group", callback_data="help_group"),
                InlineKeyboardButton("🔐 Owner", callback_data="help_sudo"),
            ],
            [InlineKeyboardButton("🔙 Back", callback_data="return_start")],
        ]
    )


def get_back_keyboard():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔙 Back", callback_data="help_main")]]
    )

# =========================
# 🚀 START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    ensure_user_exists(user)
    track_group(chat, user)

    caption = (
        f"🌷 <b>Heyyy~</b> {get_mention(user)} 🥰\n"
        f"<i>I was waiting for you 💕</i>\n\n"
        f"✨ <b>{BOT_NAME}</b> ✨\n"
        f"<i>Your Desi + Anime AI Girlfriend 🤍</i>\n\n"
        f"💖 <b>What I Can Do:</b>\n"
        f"➤ Romantic & Flirty Chats 😘\n"
        f"➤ Marriage • Couple • Love 💍\n"
        f"➤ AI Games • RPG Battles ⚔️\n"
        f"➤ Coins • XP • Leaderboards 🏆\n"
        f"➤ Cute Wishes & Jealous Mode 😒\n\n"
        f"🫶 <i>Use buttons below baby~</i>"
    )

    keyboard = get_start_keyboard(context.bot.username)

    if update.callback_query:
        try:
            await update.callback_query.message.edit_media(
                InputMediaPhoto(
                    media=START_IMG_URL,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                ),
                reply_markup=keyboard,
            )
        except Exception:
            await update.callback_query.message.edit_caption(
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
            )
    else:
        if START_IMG_URL:
            try:
                await update.message.reply_photo(
                    photo=START_IMG_URL,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=keyboard,
                )
            except Exception:
                await update.message.reply_text(
                    caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=keyboard,
                )
        else:
            await update.message.reply_text(
                caption,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
            )

    if chat.type == ChatType.PRIVATE and not update.callback_query:
        await log_to_channel(
            context.bot,
            "command",
            {
                "user": f"{get_mention(user)} (`{user.id}`)",
                "action": "Started Bot",
                "chat": "Private",
            },
        )

# =========================
# 📖 HELP COMMAND
# =========================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=HELP_IMG_URL,
        caption=(
            f"📖 <b>{BOT_NAME} Help Menu</b> 🌸\n\n"
            f"<i>Select what you want, jaan~ 💕</i>"
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=get_help_keyboard(),
    )

# =========================
# 🖱️ CALLBACK HANDLER
# =========================

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "return_start":
        await start(update, context)
        return

    if data == "help_main":
        await query.message.edit_media(
            InputMediaPhoto(
                media=HELP_IMG_URL,
                caption=(
                    f"📖 <b>{BOT_NAME} Help Menu</b> 🌸\n\n"
                    f"<i>Select what you want, jaan~ 💕</i>"
                ),
                parse_mode=ParseMode.HTML,
            ),
            reply_markup=get_help_keyboard(),
        )
        return

    photo = HELP_IMG_URL
    keyboard = get_back_keyboard()

    if data == "help_social":
        text = (
            "💍 <b>Love & Relationship</b> 💕\n\n"
            "➤ <b>/propose @user</b> — Cute proposal 💌\n"
            "➤ <b>/marry</b> — Relationship status 🥰\n"
            "➤ <b>/divorce</b> — Breakup 💔\n"
            "➤ <b>/couple</b> — Matchmaking ✨"
        )

    elif data == "help_economy":
        text = (
            "💰 <b>Economy & Rewards</b>\n\n"
            "➤ <b>/bal</b> — Wallet & Rank\n"
            "➤ <b>/shop</b> — Buy items 🛒\n"
            "➤ <b>/give</b> — Send coins 💸\n"
            "➤ <b>/daily</b> — Daily reward 🎁\n"
            "➤ <b>/ranking</b> — Leaderboard 🏆"
        )

    elif data == "help_rpg":
        text = (
            "⚔️ <b>RPG & Battles</b>\n\n"
            "➤ <b>/kill</b> — Attack enemy 🔪\n"
            "➤ <b>/rob</b> — Steal coins 🕵️\n"
            "➤ <b>/protect</b> — Shield 🛡️\n"
            "➤ <b>/revive</b> — Revive 💉"
        )

    elif data == "help_fun":
        text = (
            "🧠 <b>AI & Fun</b> 🤖💖\n\n"
            "➤ <b>/chatbot</b> — Girlfriend mode 😘\n"
            "➤ <b>/draw</b> — AI art 🎨\n"
            "➤ <b>/speak</b> — Voice 🎤\n"
            "➤ <b>/riddle</b> — Quiz 🧩"
        )

    elif data == "help_group":
        text = (
            "⚙️ <b>Group Settings</b>\n\n"
            "➤ <b>/welcome on/off</b>\n"
            "➤ <b>/ping</b> — Bot status"
        )

    elif data == "help_sudo":
        if query.from_user.id not in SUDO_USERS:
            return await query.answer("❌ Owner only!", show_alert=True)
        photo = SUDO_IMG
        text = (
            "🔐 <b>Owner Panel</b> 👑\n\n"
            "➤ Add / Remove coins\n"
            "➤ Broadcast messages\n"
            "➤ Restart bot\n"
            "➤ Database clean"
        )

    await query.message.edit_media(
        InputMediaPhoto(
            media=photo,
            caption=text,
            parse_mode=ParseMode.HTML,
        ),
        reply_markup=keyboard,
    )
