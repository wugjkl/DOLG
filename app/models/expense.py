import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    paid_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, default="General", nullable=False)
    split_type = Column(String, default="equal", nullable=False)  # "equal" or "exact"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    group = relationship("Group", back_populates="expenses")
    payer = relationship("User", foreign_keys=[paid_by], back_populates="expenses_paid")
    shares = relationship("ExpenseShare", back_populates="expense", cascade="all, delete-orphan")


class ExpenseShare(Base):
    __tablename__ = "expense_shares"

    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    share_amount = Column(Float, nullable=False)

    # Relationships
    expense = relationship("Expense", back_populates="shares")
    user = relationship("User", back_populates="expense_shares")
