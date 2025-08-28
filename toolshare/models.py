from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Date, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base
import enum

class LoanStatus(enum.Enum):
    requested = "requested"
    approved = "approved"
    rejected = "rejected"
    active = "active"
    returned = "returned"
    cancelled = "cancelled"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tools = relationship("Tool", back_populates="owner", cascade="all,delete-orphan")
    loans = relationship("Loan", back_populates="borrower", cascade="all,delete-orphan")

class Tool(Base):
    __tablename__ = "tools"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(256), nullable=False)
    description = Column(Text, default="")
    daily_rate = Column(Float, nullable=False, default=0.0)
    category = Column(String(128), default="")
    condition = Column(String(64), default="good")
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="tools")
    loans = relationship("Loan", back_populates="tool", cascade="all,delete-orphan")

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True)
    tool_id = Column(Integer, ForeignKey("tools.id"), nullable=False)
    borrower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Enum(LoanStatus), nullable=False, default=LoanStatus.requested)
    total_cost = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    tool = relationship("Tool", back_populates="loans")
    borrower = relationship("User", back_populates="loans")
