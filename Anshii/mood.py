import random
from baka.database import xp_collection, relationship_collection

MOODS = {
    "happy": [
        "🥰 Aaj mood bohot acha hai jaan",
        "Tumse baat karke smile aa gayi 💕",
    ],
    "normal": [
        "Hmm bolo na 🙂",
        "Sun rahi hoon tumhe",
    ],
    "angry": [
        "😒 Abhi mood thoda off hai",
        "Baad me baat karte hain",
    ],
    "sad": [
        "😔 Pata nahi mann kyu udaas hai",
        "Tum badal gaye ho shayad…",
    ],
}

def get_mood(user_id: int, bot_id: int):
    xp = xp_collection.find_one({"user_id": user_id})
    xp = xp.get("xp", 0) if xp else 0

    relation = relationship_collection.find_one(
        {"$or": [{"user1": user_id}, {"user2": user_id}]}
    )

    if not relation:
        return "sad"

    if xp > 500:
        return "happy"
    elif xp > 100:
        return "normal"
    else:
        return "angry"

def mood_reply(user_id: int, bot_id: int):
    mood = get_mood(user_id, bot_id)
    return random.choice(MOODS[mood])
