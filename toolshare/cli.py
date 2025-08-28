import click
from datetime import datetime
from toolshare.db import init_db, SessionLocal
from toolshare import services
from toolshare.models import LoanStatus

@click.group()
def cli():
    """ToolShare CLI"""
    pass

@cli.command()
def initdb():
    """Initialize the database."""
    init_db()
    click.echo("Database initialized successfully.")

@cli.command()
@click.argument("username")
@click.argument("password")
def add_user(username, password):
    """Add a new user."""
    db = SessionLocal()
    try:
        user = services.create_user(db, username, password)
        click.echo(f"Created user {user.username} with ID {user.id}")
    except Exception as e:
        click.echo(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

@cli.command()
def list_users():
    """List all users."""
    db = SessionLocal()
    users = services.list_users(db)
    for user in users:
        click.echo(f"{user.id}: {user.username}")
    db.close()

@cli.command()
@click.argument("owner_id", type=int)
@click.argument("title")
@click.argument("daily_rate", type=float)
@click.option("--description", default="")
@click.option("--category", default="")
@click.option("--condition", default="good")
def add_tool(owner_id, title, daily_rate, description, category, condition):
    """Add a new tool."""
    db = SessionLocal()
    try:
        tool = services.create_tool(db, owner_id, title, daily_rate, description, category, condition)
        click.echo(f"Created tool {tool.title} with ID {tool.id}")
    except Exception as e:
        click.echo(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

@cli.command()
def list_tools():
    """List all tools."""
    db = SessionLocal()
    tools = services.list_tools(db)
    for tool in tools:
        click.echo(f"{tool.id}: {tool.title} (Owner ID: {tool.owner_id})")
    db.close()

@cli.command()
@click.argument("tool_id", type=int)
@click.argument("borrower_id", type=int)
@click.argument("start_date")
@click.argument("end_date")
def create_loan(tool_id, borrower_id, start_date, end_date):
    """Create a loan for a tool."""
    db = SessionLocal()
    try:
        loan = services.create_loan(db, tool_id, borrower_id, start_date, end_date)
        click.echo(f"Created loan ID {loan.id} from {loan.start_date} to {loan.end_date}, Total cost: {loan.total_cost}")
    except Exception as e:
        click.echo(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

@cli.command()
def list_loans():
    """List all loans."""
    db = SessionLocal()
    loans = services.list_loans(db)
    for loan in loans:
        click.echo(f"{loan.id}: Tool ID {loan.tool_id}, Borrower ID {loan.borrower_id}, Status: {loan.status.value}, Total Cost: {loan.total_cost}")
    db.close()

@cli.command()
@click.argument("loan_id", type=int)
@click.argument("new_status")
def update_loan(loan_id, new_status):
    """Update the status of a loan."""
    db = SessionLocal()
    try:
        status_enum = LoanStatus(new_status)
        loan = services.update_loan_status(db, loan_id, status_enum)
        click.echo(f"Loan ID {loan.id} status updated to {loan.status.value}")
    except ValueError as e:
        click.echo(f"Error: {e}")
        db.rollback()
    except Exception as e:
        click.echo(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cli()
