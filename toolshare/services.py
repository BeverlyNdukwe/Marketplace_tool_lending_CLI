from sqlalchemy.orm import Session
from datetime import datetime
from .models import User, Tool, Loan, LoanStatus

def create_user(db: Session, username: str, password: str):
    """Create a new user."""
    user = User(username=username, password_hash=password)  # ⚠️ plain text, hash later if needed
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def list_users(db: Session):
    """Return all users."""
    return db.query(User).all()

def create_tool(db: Session, owner_id: int, title: str, daily_rate: float,
                description: str = "", category: str = "", condition: str = "good"):
    """Create a new tool for a user."""
    owner = db.query(User).filter(User.id == owner_id).first()
    if not owner:
        raise ValueError(f"User with id {owner_id} does not exist.")

    tool = Tool(
        owner_id=owner_id,
        title=title,
        description=description,
        daily_rate=daily_rate,
        category=category,
        condition=condition,
    )
    db.add(tool)
    db.commit()
    db.refresh(tool)
    return tool

def list_tools(db: Session):
    """Return all tools."""
    return db.query(Tool).all()

def create_loan(db: Session, tool_id: int, borrower_id: int,
                start_date: str, end_date: str):
    """Create a loan for a tool between dates."""
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    borrower = db.query(User).filter(User.id == borrower_id).first()

    if not tool:
        raise ValueError(f"Tool with id {tool_id} does not exist.")
    if not borrower:
        raise ValueError(f"User with id {borrower_id} does not exist.")

    start = datetime.strptime(start_date, "%Y-%m-%d").date() if isinstance(start_date, str) else start_date
    end = datetime.strptime(end_date, "%Y-%m-%d").date() if isinstance(end_date, str) else end_date

    if end <= start:
        raise ValueError("End date must be after start date.")

    days = (end - start).days
    total_cost = days * tool.daily_rate

    loan = Loan(
        tool_id=tool_id,
        borrower_id=borrower_id,
        start_date=start,
        end_date=end,
        status=LoanStatus.requested,
        total_cost=total_cost,
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def list_loans(db: Session):
    """Return all loans."""
    return db.query(Loan).all()

def update_loan_status(db: Session, loan_id: int, new_status: LoanStatus):
    """Update loan status (approved, rejected, returned, etc.)."""
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise ValueError(f"Loan with id {loan_id} does not exist.")

    loan.status = new_status
    db.commit()
    db.refresh(loan)
    return loan