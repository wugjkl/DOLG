from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.user import UserResponse


class ExpenseShareInput(BaseModel):
    user_id: int
    share_amount: float = Field(gt=0, description="Amount owed by this user")


class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0, description="Total expense amount")
    description: str
    category: str = "General"
    split_type: str = "equal"  # "equal" or "exact"
    participant_ids: Optional[List[int]] = None  # If equal split: specify user_ids involved (defaults to all members)
    shares: Optional[List[ExpenseShareInput]] = None  # If exact split: explicit user_id -> amount list


class ExpenseShareItem(BaseModel):
    id: int
    user_id: int
    share_amount: float
    user: UserResponse

    class Config:
        from_attributes = True


class ExpenseResponse(BaseModel):
    id: int
    group_id: int
    paid_by: int
    payer: UserResponse
    amount: float
    description: str
    category: str
    split_type: str
    created_at: datetime
    shares: List[ExpenseShareItem] = []

    class Config:
        from_attributes = True
