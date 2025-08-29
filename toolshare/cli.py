import sys
from sqlalchemy.orm import Session
from .db import get_db, init_db
from . import services


def _prompt_choice(prompt, choices):
    """Ask the user to pick from a list of choices."""
    print(f"\n{prompt}")
    for i, choice in enumerate(choices, start=1):
        print(f"{i}. {choice}")
    while True:
        try:
            selection = int(input("Enter number: "))
            if 1 <= selection <= len(choices):
                return choices[selection - 1]
            else:
                print("Invalid choice, try again.")
        except ValueError:
            print("Please enter a number.")


def add_user():
    with next(get_db()) as db:
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = services.create_user(db, username, password)
        print(f"User created: {user.username} (id={user.id})")


def list_users():
    with next(get_db()) as db:
        users = services.list_users(db)
        print("\n--- Users ---")
        for u in users:
            print(f"[{u.id}] {u.username}")


def add_tool():
    with next(get_db()) as db:
        owner_id = int(input("Enter owner ID: "))
        title = input("Enter tool title: ")
        rate = float(input("Enter daily rate: "))
        desc = input("Enter description: ")
        category = input("Enter category: ")
        condition = input("Enter condition (good/new/old): ")
        tool = services.create_tool(db, owner_id, title, rate, desc, category, condition)
        print(f"Tool created: {tool.title} (id={tool.id})")


def list_tools():
    with next(get_db()) as db:
        tools = services.list_tools(db)
        print("\n--- Tools ---")
        for t in tools:
            print(f"[{t.id}] {t.title} - Owner {t.owner_id}, {t.daily_rate}/day")


def create_loan():
    with next(get_db()) as db:
        tool_id = int(input("Enter tool ID: "))
        borrower_id = int(input("Enter borrower ID: "))
        start = input("Enter start date (YYYY-MM-DD): ")
        end = input("Enter end date (YYYY-MM-DD): ")
        loan = services.create_loan(db, tool_id, borrower_id, start, end)
        print(f"Loan created: Tool {loan.tool_id} to User {loan.borrower_id}, Total = {loan.total_cost}")


def list_loans():
    with next(get_db()) as db:
        loans = services.list_loans(db)
        print("\n--- Loans ---")
        for l in loans:
            print(f"[{l.id}] Tool {l.tool_id} → User {l.borrower_id}, {l.start_date} to {l.end_date}, Status={l.status}, Cost={l.total_cost}")


def main_menu():
    print(" Welcome to ToolShare CLI ")
    print("Database initialized automatically if empty.\n")

    while True:
        choice = _prompt_choice("What would you like to do?", [
            "Add User",
            "List Users",
            "Add Tool",
            "List Tools",
            "Create Loan",
            "List Loans",
            "Exit"
        ])

        if choice == "Add User":
            add_user()
        elif choice == "List Users":
            list_users()
        elif choice == "Add Tool":
            add_tool()
        elif choice == "List Tools":
            list_tools()
        elif choice == "Create Loan":
            create_loan()
        elif choice == "List Loans":
            list_loans()
        elif choice == "Exit":
            print("Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    init_db()
    main_menu()
