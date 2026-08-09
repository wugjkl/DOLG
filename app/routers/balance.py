from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.group import GroupMember
from app.models.settlement import Settlement
from app.schemas.balance import (
    GroupBalanceResponse,
    TransactionSuggestion,
    SettlementCreate,
    SettlementResponse
)
from app.core.dependencies import get_current_user
from app.routers.groups import verify_group_membership
from app.services.debt_solver import calculate_group_balances, solve_greedy_debt_minimization

router = APIRouter(prefix="/groups/{group_id}", tags=["Balance & Settlements"])


@router.get("/balance", response_model=GroupBalanceResponse)
def get_group_balance(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_group_membership(group_id, current_user.id, db)
    return calculate_group_balances(db, group_id)


@router.get("/settle-up", response_model=List[TransactionSuggestion])
def get_greedy_settle_up_plan(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_group_membership(group_id, current_user.id, db)
    balances = calculate_group_balances(db, group_id)
    return solve_greedy_debt_minimization(balances)


@router.post("/settlements", response_model=SettlementResponse, status_code=status.HTTP_201_CREATED)
def record_settlement(
    group_id: int,
    settlement_in: SettlementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_group_membership(group_id, current_user.id, db)

    # Check payee is a group member
    payee_membership = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == settlement_in.payee_id
    ).first()
    if not payee_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payee (User ID {settlement_in.payee_id}) is not a member of this group"
        )

    if settlement_in.payee_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot record a settlement to yourself"
        )

    if settlement_in.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Settlement amount must be greater than zero"
        )

    settlement = Settlement(
        group_id=group_id,
        payer_id=current_user.id,
        payee_id=settlement_in.payee_id,
        amount=round(settlement_in.amount, 2)
    )
    db.add(settlement)
    db.commit()
    db.refresh(settlement)
    return settlement
