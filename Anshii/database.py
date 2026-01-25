from pymongo import MongoClient
import certifi
from Anshi.config import MONGO_URI

# Initialize Mongo Connection
Anshi = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = Anshi["anshibot_db"]

# ===============================
# CORE COLLECTIONS
# ===============================

users_collection = db["users"]                 # balance, inventory, xp, stats
groups_collection = db["groups"]               # group settings
sudoers_collection = db["sudoers"]             # sudo admins
chatbot_collection = db["chatbot"]             # AI chat history
riddles_collection = db["riddles"]             # riddles
relationship_collection = db.relationships
couple_battle_collection = db.couple_battles
subscription_collection = db.subscription
subscription_collection.create_index("user_id", unique=True)

# ===============================
# 🔐 SUBSCRIPTION / PREMIUM
# ===============================

pending_payments_collection = db["pending_payments"]
subscription_collection = db["subscriptions"]  # premium users

# {
#   user_id,
#   plan: free / silver / gold / lifetime
#   expiry,
#   activated_at
# }

# ===============================
# 🧠 MEMORY SYSTEM
# ===============================

memory_collection = db["memory"]                # AI memory per user
# {
#   user_id,
#   memories: [],
#   last_updated
# }

memory_helper_collection = db["memory_helper"]  # summarized memory
# {
#   user_id,
#   summary
# }

# ===============================
# 💕 RELATIONSHIP SYSTEM
# ===============================

relationship_collection = db["relationships"]
# {
#   user1,
#   user2,
#   status: dating/married/breakup
#   started_at
# }

marriage_proposals = db["marriage_proposals"]
auto_marriage_collection = db["auto_marriage"]

# ===============================
# 😈 MODES
# ===============================

jealous_mode_collection = db["jealous_mode"]
breakup_mode_collection = db["breakup_mode"]

# ===============================
# 🎮 XP & LEADERBOARD
# ===============================

xp_collection = db["xp"]
# {
#   user_id,
#   xp,
#   level
# }

xp_leaderboard = db["xp_leaderboard"]

# ===============================
# 🎯 COUPLE GAMES
# ===============================

couple_games_collection = db["couple_games"]
couple_battles_collection = db["couple_battles"]
dating_rooms_collection = db["dating_rooms"]

# ===============================
# 🧾 LOGGER
# ===============================

logs_collection = db["logs"]

# ===============================
# 🤖 AI ENGINE SETTINGS
# ===============================

ai_settings_collection = db["ai_settings"]

# ===============================
# 📌 INDEXES (Performance + Safety)
# ===============================

users_collection.create_index("user_id", unique=True)
subscription_collection.create_index("user_id", unique=True)
relationship_collection.create_index(
    [("user1", 1), ("user2", 1)],
    unique=True
)
xp_collection.create_index("user_id", unique=True)
