import time
from anshi.database import xp_collection
from anshi.config import XP_PER_MESSAGE, XP_COOLDOWN_SECONDS, LEVEL_MULTIPLIER

# user_id -> last xp time (memory cache)
_last_xp_time = {}

def calculate_level(total_xp: int) -> int:
    """
    XP se level calculate karta hai
    """
    level = 1
    required_xp = 100

    while total_xp >= required_xp:
        total_xp -= required_xp
        level += 1
        required_xp = int(required_xp * LEVEL_MULTIPLIER)

    return level


def award_xp(user_id: int) -> bool:
    """
    User ko XP deta hai (cooldown ke saath)
    """
    now = time.time()
    last_time = _last_xp_time.get(user_id, 0)

    # Cooldown check
    if now - last_time < XP_COOLDOWN_SECONDS:
        return False

    _last_xp_time[user_id] = now

    doc = xp_collection.find_one({"user_id": user_id}) or {
        "user_id": user_id,
        "xp": 0,
        "level": 1
    }

    new_xp = doc["xp"] + XP_PER_MESSAGE
    new_level = calculate_level(new_xp)

    xp_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "xp": new_xp,
                "level": new_level
            }
        },
        upsert=True
    )

    return True
