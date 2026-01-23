from anshi.database import xp_collection, subscription_collection

def award_xp(user_id: int):
    base_xp = 1

    sub = subscription_collection.find_one({"user_id": user_id})
    boost = sub.get("xp_boost", 1) if sub else 1

    total_xp = base_xp * boost

    xp_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"xp": total_xp}},
        upsert=True
    )
