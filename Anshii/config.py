import os

# ================= BASIC =================
BOT_NAME = os.getenv("BOT_NAME", "ᴀɴꜱʜɪᴋᴀ")
OWNER_ID = int(os.getenv("OWNER_ID", "8211189367"))  # admin telegram id

# ================= TELEGRAM =================
BOT_TOKEN = os.getenv("8539332040:AAEwLvW469kL0L7a7aCv9EA3V6MN8ZX76jQ")
PORT = int(os.getenv("PORT", "8000"))

# ================= DATABASE =================
MONGO_URI = os.getenv("MONGO_URI")

# ================= AI ENGINE =================
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "mistral-free-latest")

# ================= PAYMENT / UPI =================
UPI_ID = os.getenv("UPI_ID", "yourupi@paytm")
UPI_NAME = os.getenv("UPI_NAME", "LoveNanshi Premium")

# ================= SUBSCRIPTION =================
MONTHLY_PRICE = int(os.getenv("MONTHLY_PRICE", "99"))
YEARLY_PRICE = int(os.getenv("YEARLY_PRICE", "999"))

PLANS = {
    "monthly": 30,
    "yearly": 365
}

# ================= LOGGER =================
LOGGER_GROUP = int(os.getenv("LOGGER_GROUP", "-1003605595874"))  # optional

# ================= OTHER SETTINGS =================
AUTO_REPLY = True
PREMIUM_ONLY_FLIRT = True


# Game Constants
REVIVE_COST = 500
PROTECT_1D_COST = 1000
PROTECT_2D_COST = 1800
REGISTER_BONUS = 5000
CLAIM_BONUS = 2000
RIDDLE_REWARD = 1000
DIVORCE_COST = 2000
WAIFU_PROPOSE_COST = 5000
TAX_RATE = 0.10
MARRIED_TAX_RATE = 0.05
AUTO_REVIVE_HOURS = 6
AUTO_REVIVE_BONUS = 200
ITEM_EXPIRY_HOURS = 24 
MIN_CLAIM_MEMBERS = 100

# --- 🛒 BALANCED SHOP ITEMS (Max 60%) ---
SHOP_ITEMS = [
    # WEAPONS (Damage Buff - Increases Kill Reward)
    {"id": "stick", "name": "🪵 Stick", "price": 500, "type": "weapon", "buff": 0.01},
    {"id": "brick", "name": "🧱 Brick", "price": 1000, "type": "weapon", "buff": 0.02},
    {"id": "slingshot", "name": "🪃 Slingshot", "price": 2000, "type": "weapon", "buff": 0.03},
    {"id": "knife", "name": "🔪 Knife", "price": 3500, "type": "weapon", "buff": 0.05},
    {"id": "bat", "name": "🏏 Bat", "price": 5000, "type": "weapon", "buff": 0.08},
    {"id": "axe", "name": "🪓 Axe", "price": 7500, "type": "weapon", "buff": 0.10},
    {"id": "hammer", "name": "🔨 Hammer", "price": 10000, "type": "weapon", "buff": 0.12},
    {"id": "chainsaw", "name": "🪚 Chainsaw", "price": 15000, "type": "weapon", "buff": 0.15},
    {"id": "pistol", "name": "🔫 Pistol", "price": 25000, "type": "weapon", "buff": 0.20},
    {"id": "shotgun", "name": "🧨 Shotgun", "price": 40000, "type": "weapon", "buff": 0.25},
    {"id": "uzi", "name": "🔫 Uzi", "price": 55000, "type": "weapon", "buff": 0.30},
    {"id": "katana", "name": "⚔️ Katana", "price": 75000, "type": "weapon", "buff": 0.35},
    {"id": "ak47", "name": "💥 AK-47", "price": 100000, "type": "weapon", "buff": 0.40},
    {"id": "minigun", "name": "🔥 Minigun", "price": 150000, "type": "weapon", "buff": 0.45},
    {"id": "sniper", "name": "🎯 Sniper", "price": 200000, "type": "weapon", "buff": 0.50},
    {"id": "rpg", "name": "🚀 RPG", "price": 300000, "type": "weapon", "buff": 0.55},
    {"id": "tank", "name": "🚜 Tank", "price": 500000, "type": "weapon", "buff": 0.58},
    {"id": "laser", "name": "⚡ Laser", "price": 800000, "type": "weapon", "buff": 0.59},
    {"id": "deathnote", "name": "📓 Death Note", "price": 5000000, "type": "weapon", "buff": 0.60}, # Max Dmg

    # ARMOR (Block Chance - Stops Robberies)
    {"id": "paper", "name": "📰 Newspaper", "price": 500, "type": "armor", "buff": 0.01},
    {"id": "cardboard", "name": "📦 Cardboard", "price": 1000, "type": "armor", "buff": 0.02},
    {"id": "cloth", "name": "👕 Cloth", "price": 2500, "type": "armor", "buff": 0.05},
    {"id": "leather", "name": "🧥 Leather", "price": 8000, "type": "armor", "buff": 0.08},
    {"id": "chain", "name": "⛓️ Chain", "price": 20000, "type": "armor", "buff": 0.10},
    {"id": "riot", "name": "🛡️ Riot Shield", "price": 40000, "type": "armor", "buff": 0.15},
    {"id": "swat", "name": "👮 SWAT", "price": 60000, "type": "armor", "buff": 0.20},
    {"id": "iron", "name": "🦾 Iron Suit", "price": 100000, "type": "armor", "buff": 0.25},
    {"id": "diamond", "name": "💎 Diamond", "price": 200000, "type": "armor", "buff": 0.30},
    {"id": "obsidian", "name": "⚫ Obsidian", "price": 400000, "type": "armor", "buff": 0.35},
    {"id": "nano", "name": "🧬 Nano Suit", "price": 700000, "type": "armor", "buff": 0.40},
    {"id": "vibranium", "name": "🛡️ Vibranium", "price": 1500000, "type": "armor", "buff": 0.50},
    {"id": "force", "name": "🔮 Forcefield", "price": 3000000, "type": "armor", "buff": 0.55},
    {"id": "plot", "name": "🎬 Plot Armor", "price": 10000000, "type": "armor", "buff": 0.60}, # Max Block

    # FLEX (Safe Assets - Burn on Death)
    {"id": "cookie", "name": "🍪 Cookie", "price": 100, "type": "flex", "buff": 0},
    {"id": "coffee", "name": "☕ Starbucks", "price": 300, "type": "flex", "buff": 0},
    {"id": "rose", "name": "🌹 Rose", "price": 500, "type": "flex", "buff": 0},
    {"id": "sushi", "name": "🍣 Sushi Platter", "price": 2000, "type": "flex", "buff": 0},
    {"id": "vodka", "name": "🍾 Vodka", "price": 5000, "type": "flex", "buff": 0},
    {"id": "ring", "name": "💍 Gold Ring", "price": 10000, "type": "flex", "buff": 0},
    {"id": "ps5", "name": "🎮 PS5 Pro", "price": 15000, "type": "flex", "buff": 0},
    {"id": "iphone", "name": "📱 iPhone 16 Pro", "price": 25000, "type": "flex", "buff": 0},
    {"id": "macbook", "name": "💻 MacBook M3", "price": 50000, "type": "flex", "buff": 0},
    {"id": "gucci", "name": "👜 Gucci Bag", "price": 75000, "type": "flex", "buff": 0},
    {"id": "rolex", "name": "⌚ Rolex", "price": 100000, "type": "flex", "buff": 0},
    {"id": "diamond_ring", "name": "💎 Solitaire", "price": 250000, "type": "flex", "buff": 0},
    {"id": "tesla", "name": "🚗 Tesla", "price": 400000, "type": "flex", "buff": 0},
    {"id": "lambo", "name": "🏎️ Lambo", "price": 800000, "type": "flex", "buff": 0},
    {"id": "heli", "name": "🚁 Helicopter", "price": 1500000, "type": "flex", "buff": 0},
    {"id": "yacht", "name": "🛳️ Super Yacht", "price": 3000000, "type": "flex", "buff": 0},
    {"id": "mansion", "name": "🏰 Mansion", "price": 5000000, "type": "flex", "buff": 0},
    {"id": "jet", "name": "✈️ Private Jet", "price": 10000000, "type": "flex", "buff": 0},
    {"id": "island", "name": "🏝️ Private Island", "price": 50000000, "type": "flex", "buff": 0},
    {"id": "moon", "name": "🌑 The Moon", "price": 100000000, "type": "flex", "buff": 0},
    {"id": "mars", "name": "🪐 Mars", "price": 500000000, "type": "flex", "buff": 0},
    {"id": "sun", "name": "☀️ The Sun", "price": 1000000000, "type": "flex", "buff": 0},
    {"id": "galaxy", "name": "🌌 Milky Way", "price": 5000000000, "type": "flex", "buff": 0},
    {"id": "blackhole", "name": "🕳️ Black Hole", "price": 9999999999, "type": "flex", "buff": 0},
]

# =========================
# ❤️ RELATIONSHIP / LOVE SYSTEM
# =========================

AUTO_MARRIAGE_ENABLED = True
JEALOUS_MODE_ENABLED = True
BREAKUP_MODE_ENABLED = True
RELATIONSHIP_XP_BONUS = 50
AUTO_PROPOSAL_CHANCE = 0.05   # 5% chance per chat


# =========================
# 🧠 XP / LEVEL SYSTEM
# =========================

XP_PER_MESSAGE = 5
XP_PER_COUPLE_GAME = 50
XP_PER_BATTLE_WIN = 100
XP_COOLDOWN_SECONDS = 60

LEVEL_MULTIPLIER = 1.5


# =========================
# 🏆 LEADERBOARD
# =========================

LEADERBOARD_LIMIT = 10
LEADERBOARD_REFRESH_TIME = 300  # seconds


# =========================
# 💎 SUBSCRIPTION / PREMIUM
# =========================

PREMIUM_MONTHLY_COST = 199
PREMIUM_YEARLY_COST = 999

PREMIUM_FEATURES = [
    "jealous_mode",
    "auto_marriage",
    "dating_rooms",
    "couple_battle",
    "memory_boost",
    "ai_priority_reply"
]


# =========================
# 🧠 MEMORY / LOGGER
# =========================

MEMORY_LIMIT_FREE = 20
MEMORY_LIMIT_PREMIUM = 100

SAVE_RELATIONSHIP_MEMORY = True
SAVE_CHAT_MEMORY = True

LOG_RELATIONSHIPS = True
LOG_PREMIUM_ACTIONS = True


# =========================
# 🤖 AI / GIRLFRIEND MODE
# =========================

AI_GIRLFRIEND_MODE = True
AI_FLIRT_LEVEL = "HIGH"   # LOW | MEDIUM | HIGH
AI_REPLY_DELAY = (1, 3)   # seconds (min, max)

INDIAN_GIRLFRIEND_STYLE = True
UNLIMITED_AUTO_REPLY = True

