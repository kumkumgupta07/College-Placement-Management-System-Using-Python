# auth/auth_utils.py

import bcrypt
from utils.database import get_db
def _is_valid_email(email: str) -> bool:
    return isinstance(email, str) and email.endswith("@gmail.com")


def _hash_password(plain: str) -> bytes:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())

def _check_password(plain: str, hashed) -> bool:
    # handle str/bytes from DB
    if isinstance(hashed, str):
        hashed = hashed.encode("utf-8")
    return bcrypt.checkpw(plain.encode("utf-8"), hashed)

def login_user(email, password):
    db = get_db()
    if not _is_valid_email(email):
        return None
    user = db.users.find_one({"email": email})
    if not user:
        return None

    # New path: hashed password present
    if "password_hash" in user:
        if _check_password(password, user["password_hash"]):
            user.pop("password_hash", None)
            user.pop("password", None)  # just in case
            return user
        return None

    # Legacy path: plaintext password present -> verify then migrate
    if "password" in user and user["password"] == password:
        hashed = _hash_password(password).decode("utf-8")
        db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"password_hash": hashed}, "$unset": {"password": ""}}
        )
        user.pop("password", None)
        user["password_hash"] = hashed
        return user

    return None

def register_user(name, email, password, role):
    db = get_db()
    if not _is_valid_email(email):
        return False
    if db.users.find_one({"email": email}):
        return False

    hashed = _hash_password(password).decode("utf-8")
    db.users.insert_one({
        "name": name,
        "email": email,
        "password_hash": hashed,
        "role": role,
        "resume_path": None,
        "activity_log": [],
        "notifications": []
    })
    return True
