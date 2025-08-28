import hashlib
import json
from pathlib import Path
from typing import Optional
from .db import SessionLocal
from .models import User
from sqlalchemy.exc import IntegrityError
from datetime import datetime

SESSION_PATH = Path.home() / ".toolshare_session.json"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash

def set_session_user_id(user_id: int) -> None:
    SESSION_PATH.write_text(json.dumps({"user_id": user_id}))

def get_session_user_id() -> Optional[int]:
    if not SESSION_PATH.exists():
        return None
    try:
        data = json.loads(SESSION_PATH.read_text() or "{}")
        return data.get("user_id")
    except Exception:
        return None

def clear_session() -> None:
    try:
        SESSION_PATH.unlink(missing_ok=True)
    except Exception:
        pass

def require_login() -> int:
    uid = get_session_user_id()
    if uid is None:
        raise SystemExit("You are not logged in. Run: toolshare login --username <u> --password <p>")
    return uid

def create_user(username: str, password: str):
    db = SessionLocal()
    try:
        user = User(username=username, password_hash=hash_password(password), created_at=datetime.utcnow())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user.id
    except IntegrityError:
        db.rollback()
        raise SystemExit("Username already exists.")
    finally:
        db.close()

def authenticate(username: str, password: str) -> int:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password_hash):
            raise SystemExit("Invalid username or password.")
        return user.id
    finally:
        db.close()
