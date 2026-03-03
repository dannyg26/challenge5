from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from .db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    investments = relationship("Investment", back_populates="user", cascade="all, delete-orphan")
    mortgage = relationship("Mortgage", back_populates="user", uselist=False, cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)  # +income, -expense
    category: Mapped[str] = mapped_column(String(80), default="general")
    description: Mapped[str] = mapped_column(String(255), default="")
    user = relationship("User", back_populates="transactions")

class Investment(Base):
    __tablename__ = "investments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    ticker: Mapped[str] = mapped_column(String(20), nullable=False)
    shares: Mapped[float] = mapped_column(Float, default=0.0)
    avg_cost: Mapped[float] = mapped_column(Float, default=0.0)
    notes: Mapped[str] = mapped_column(Text, default="")
    user = relationship("User", back_populates="investments")
    __table_args__ = (UniqueConstraint("user_id", "ticker", name="uq_user_ticker"),)

class Mortgage(Base):
    __tablename__ = "mortgages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, index=True)
    principal: Mapped[float] = mapped_column(Float, default=0.0)
    annual_rate: Mapped[float] = mapped_column(Float, default=0.0)
    term_months: Mapped[int] = mapped_column(Integer, default=360)
    extra_payment: Mapped[float] = mapped_column(Float, default=0.0)
    user = relationship("User", back_populates="mortgage")

class Budget(Base):
    __tablename__ = "budgets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    monthly_limit: Mapped[float] = mapped_column(Float, default=0.0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    user = relationship("User", back_populates="budgets")
    __table_args__ = (UniqueConstraint("user_id", "category", name="uq_user_budget_category"),)
