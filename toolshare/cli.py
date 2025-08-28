import click
from tabulate import tabulate
from toolshare.db import SessionLocal
from toolshare.services import create_user, list_users, create_tool, list_tools

@click.group()
def cli():
    """ToolShare CLI - A simple marketplace for lending and borrowing tools."""
    pass

# ----------------------
# Database initialization
# ----------------------
@cli.command()
def init_db():
    """Initialize the database."""
    from toolshare.db import init_db
    init_db()
    click.echo("Database initialized.")

# ----------------------
# User commands
# ----------------------
@cli.command()
@click.option("--username", prompt=True, help="Username of the new user")
@click.option("--email", prompt=True, help="Email of the new user")


def add_user(username, email):
    """Add a new user."""
    db = SessionLocal()
    user = create_user(db, username=username, email=email)
    click.echo(f" User created: {user.username} ({user.email})")

@cli.command()
def show_users():
    """Show all users."""
    db = SessionLocal()
    users = list_users(db)

    if not users:
        click.echo("No users found.")
        return

    table = [(u.id, u.username, u.email) for u in users]
    headers = ["ID", "Username", "Email"]
    click.echo(tabulate(table, headers, tablefmt="fancy_grid"))

# ----------------------
# Tool commands
# ----------------------
@cli.command()
@click.argument("owner_id", type=int)
@click.argument("name")
@click.argument("description")
def add_tool(owner_id, name, description):
    """Add a tool belonging to a user."""
    db = SessionLocal()
    tool = create_tool(db, owner_id=owner_id, name=name, description=description)
    click.echo(f"Tool added: {tool.name} (Owner ID: {tool.owner_id})")

@cli.command()
def show_tools():
    """Show all tools."""
    db = SessionLocal()
    tools = list_tools(db)

    if not tools:
        click.echo("No tools found.")
        return

    table = [(t.id, t.name, t.description, t.owner_id) for t in tools]
    headers = ["ID", "Name", "Description", "Owner ID"]
    click.echo(tabulate(table, headers, tablefmt="fancy_grid"))
