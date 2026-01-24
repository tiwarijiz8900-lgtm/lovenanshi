from datetime import datetime, timedelta
from baka.database import subscription_collection

PLANS = {
    "monthly": 30,
    "yearly": 365
}

def activate_premium(user_id: int, plan: str):
    days = PLANS.get(plan)
    if not days:
        return False

    expiry = datetime.utcnow() + timedelta(days=days)

    subscription_collection.update_one(
        {"user_id": user_id},
        {"$set": {
            "user_id": user_id,
            "plan": plan,
            "expiry": expiry
        }},
        upsert=True
    )
    return expiry


def is_premium(user_id: int) -> bool:
    data = subscription_collection.find_one({"user_id": user_id})
    if not data:
        return False

    if data["expiry"] < datetime.utcnow():
        subscription_collection.delete_one({"user_id": user_id})
        return False

    return True
