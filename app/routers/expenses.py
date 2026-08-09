from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.group import GroupMember
from app.models.expense import Expense, ExpenseShare
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.core.dependencies import get_current_user
from app.routers.groups import verify_group_membership

router = APIRouter(prefix="/groups/{group_id}/expenses", tags=["Expenses"])


@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    group_id: int,
    expense_in: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    group = verify_group_membership(group_id, current_user.id, db)

    # Fetch all group member user IDs
    members = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
    member_user_ids = {m.user_id for m in members}

    shares_to_create = []

    if expense_in.split_type == "equal":
        # Determine participants
        if expense_in.participant_ids:
            target_uids = list(set(expense_in.participant_ids))
            for uid in target_uids:
                if uid not in member_user_ids:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"User ID {uid} is not a member of this group"
                    )
        else:
            target_uids = list(member_user_ids)

        if not target_uids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No participants available to split the expense"
            )

        split_amount = round(expense_in.amount / len(target_uids), 2)
        # Adjust potential rounding difference on first share
        remainder = round(expense_in.amount - (split_amount * len(target_uids)), 2)

        for idx, uid in enumerate(target_uids):
            share_val = split_amount + (remainder if idx == 0 else 0.0)
            shares_to_create.append({"user_id": uid, "share_amount": round(share_val, 2)})

    elif expense_in.split_type == "exact":
        if not expense_in.shares:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Shares list is required for exact split strategy"
            )
        
        sum_shares = 0.0
        for item in expense_in.shares:
            if item.user_id not in member_user_ids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"User ID {item.user_id} is not a member of this group"
                )
            sum_shares += item.share_amount
            shares_to_create.append({"user_id": item.user_id, "share_amount": round(item.share_amount, 2)})

        if abs(sum_shares - expense_in.amount) > 0.01:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sum of exact shares ({sum_shares:.2f}) does not match total expense amount ({expense_in.amount:.2f})"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid split_type. Supported values: 'equal', 'exact'"
        )

    # Save expense
    expense = Expense(
        group_id=group_id,
        paid_by=current_user.id,
        amount=expense_in.amount,
        description=expense_in.description,
        category=expense_in.category,
        split_type=expense_in.split_type
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)

    # Save shares
    for s_dict in shares_to_create:
        share = ExpenseShare(
            expense_id=expense.id,
            user_id=s_dict["user_id"],
            share_amount=s_dict["share_amount"]
        )
        db.add(share)

    db.commit()
    db.refresh(expense)
    return expense


@router.get("", response_model=List[ExpenseResponse])
def get_group_expenses(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_group_membership(group_id, current_user.id, db)
    expenses = db.query(Expense).filter(Expense.group_id == group_id).order_by(Expense.created_at.desc()).all()
    return expenses


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    group_id: int,
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_group_membership(group_id, current_user.id, db)
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.group_id == group_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    if expense.paid_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the user who paid for this expense can delete it"
        )
    db.delete(expense)
    db.commit()
