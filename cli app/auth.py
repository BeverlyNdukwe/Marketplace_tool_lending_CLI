import hashlib
import json
import os
from .db import get_connection

SESSION_FILE = os.path.expanduser("~/.toolshare_session.json")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, hash_password(password)))
        conn.commit()
        print(f"✅ User {username} registered successfully.")
    except Exception as e:
        print("⚠️ Error:", e)
    finally:
        conn.close()

def login(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()

    if row and row[1] == hash_password(password):
        session = {"user_id": row[0], "username": username}
        with open(SESSION_FILE, "w") as f:
            json.dump(session, f)
        print(f"✅ Logged in as {username}")
    else:
        print("❌ Invalid credentials")

def logout():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        print("✅ Logged out.")
    else:
        print("⚠️ No active session.")

def get_current_user():
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        return json.load(f)
