import sqlite3

DB_NAME = "toolshare.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Tools table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        daily_rate REAL NOT NULL,
        available INTEGER DEFAULT 1,
        FOREIGN KEY(owner_id) REFERENCES users(id)
    )
    """)

    # Loans table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tool_id INTEGER NOT NULL,
        borrower_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY(tool_id) REFERENCES tools(id),
        FOREIGN KEY(borrower_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()
