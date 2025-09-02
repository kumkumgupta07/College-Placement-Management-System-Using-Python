# utils/notifications.py
from utils.database import get_db
from datetime import datetime

db = get_db()

def send_notification(title, message, for_role=None, for_user_id=None):
    """
    Send a notification to either a role (e.g., "Student", "College") or a specific user_id.
    """
    if not for_role and not for_user_id:
        raise ValueError("You must specify either for_role or for_user_id.")

    db.notifications.insert_one({
        "title": title,
        "message": message,
        "user_role": for_role,
        "user_id": for_user_id,
        "date": datetime.utcnow()
    })

def get_notifications_for_user(user_role=None, user_id=None):
    """
    Get notifications for a role or specific user_id.
    """
    if user_id:
        return db.notifications.find({"user_id": user_id}).sort("date", -1)
    elif user_role:
        return db.notifications.find({"user_role": user_role}).sort("date", -1)
    else:
        return []
