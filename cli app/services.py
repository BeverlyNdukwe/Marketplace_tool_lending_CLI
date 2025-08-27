from .db import get_connection
from .auth import get_current_user

def add_tool(title, description, category, daily_rate):
    user = get_current_user()
    if not user:
        print("Please login first.")
        return
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO tools (owner_id, title, description, category, daily_rate)
    VALUES (?, ?, ?, ?, ?)
    """, (user["user_id"], title, description, category, daily_rate))
    conn.commit()
    conn.close()
    print(f"✅ Tool '{title}' added.")

def list_tools(available=False, mine=False):
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT t.id, t.title, t.description, t.category, t.daily_rate, u.username FROM tools t JOIN users u ON t.owner_id = u.id"
    filters = []
    if available:
        query += " WHERE t.available=1"
    if mine:
        user = get_current_user()
        if not user:
            print(" Please login first.")
            return
        if "WHERE" in query:
            query += " AND t.owner_id=?"
        else:
            query += " WHERE t.owner_id=?"
        filters.append(user["user_id"])
    cur.execute(query, filters)
    rows = cur.fetchall()
    conn.close()
    for r in rows:
        print(f"[{r[0]}] {r[1]} - {r[2]} ({r[3]}), Rate: {r[4]} by {r[5]}")

def request_loan(tool_id, start_date, end_date):
    user = get_current_user()
    if not user:
        print(" Please login first.")
        return
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO loans (tool_id, borrower_id, start_date, end_date)
    VALUES (?, ?, ?, ?)
    """, (tool_id, user["user_id"], start_date, end_date))
    conn.commit()
    conn.close()
    print(f"✅ Loan request for tool {tool_id} submitted.")

def view_inbox():
    user = get_current_user()
    if not user:
        print(" Please login first.")
        return
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT l.id, t.title, u.username, l.start_date, l.end_date, l.status
    FROM loans l
    JOIN tools t ON l.tool_id = t.id
    JOIN users u ON l.borrower_id = u.id
    WHERE t.owner_id=?
    """, (user["user_id"],))
    rows = cur.fetchall()
    conn.close()
    for r in rows:
        print(f"[{r[0]}] {r[1]} requested by {r[2]} ({r[3]} → {r[4]}) status: {r[5]}")

def approve_loan(loan_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE loans SET status='approved' WHERE id=?", (loan_id,))
    conn.commit()
    conn.close()
    print(f"✅ Loan {loan_id} approved.")

def reject_loan(loan_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE loans SET status='rejected' WHERE id=?", (loan_id,))
    conn.commit()
    conn.close()
    print(f" Loan {loan_id} rejected.")
