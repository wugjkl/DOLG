from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.schemas.user import UserResponse


class MemberBalanceItem(BaseModel):
    user_id: int
    user_name: str
    user_email: str
    paid_total: float
    owed_total: float
    settlements_paid: float
    settlements_received: float
    net_balance: float  # paid_total - owed_total - settlements_paid + settlements_received


class GroupBalanceResponse(BaseModel):
    group_id: int
    total_group_spending: float
    members: List[MemberBalanceItem]


class TransactionSuggestion(BaseModel):
    from_user_id: int
    from_user_name: str
    to_user_id: int
    to_user_name: str
    amount: float


class SettlementCreate(BaseModel):
    payee_id: int
    amount: float


class SettlementResponse(BaseModel):
    id: int
    group_id: int
    payer_id: int
    payer: UserResponse
    payee_id: int
    payee: UserResponse
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True
