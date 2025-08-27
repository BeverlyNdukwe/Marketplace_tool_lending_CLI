import argparse
from . import db, auth, services

def main():
    parser = argparse.ArgumentParser(description="Tool Lending Marketplace CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init-db")

    reg = subparsers.add_parser("register")
    reg.add_argument("--username", required=True)
    reg.add_argument("--password", required=True)

    login = subparsers.add_parser("login")
    login.add_argument("--username", required=True)
    login.add_argument("--password", required=True)

    subparsers.add_parser("logout")

    add_tool = subparsers.add_parser("add-tool")
    add_tool.add_argument("--title", required=True)
    add_tool.add_argument("--description", required=True)
    add_tool.add_argument("--category", required=True)
    add_tool.add_argument("--daily-rate", type=float, required=True)

    list_tools = subparsers.add_parser("list-tools")
    list_tools.add_argument("--available", action="store_true")
    list_tools.add_argument("--mine", action="store_true")

    req_loan = subparsers.add_parser("request-loan")
    req_loan.add_argument("--tool-id", type=int, required=True)
    req_loan.add_argument("--start-date", required=True)
    req_loan.add_argument("--end-date", required=True)

    subparsers.add_parser("inbox")

    approve = subparsers.add_parser("approve")
    approve.add_argument("--loan-id", type=int, required=True)

    reject = subparsers.add_parser("reject")
    reject.add_argument("--loan-id", type=int, required=True)

    args = parser.parse_args()

    if args.command == "init-db":
        db.init_db()
        print("✅ Database initialized.")
    elif args.command == "register":
        auth.register(args.username, args.password)
    elif args.command == "login":
        auth.login(args.username, args.password)
    elif args.command == "logout":
        auth.logout()
    elif args.command == "add-tool":
        services.add_tool(args.title, args.description, args.category, args.daily_rate)
    elif args.command == "list-tools":
        services.list_tools(available=args.available, mine=args.mine)
    elif args.command == "request-loan":
        services.request_loan(args.tool_id, args.start_date, args.end_date)
    elif args.command == "inbox":
        services.view_inbox()
    elif args.command == "approve":
        services.approve_loan(args.loan_id)
    elif args.command == "reject":
        services.reject_loan(args.loan_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
