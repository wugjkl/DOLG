from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.group import Group, GroupMember
from app.schemas.group import (
    GroupCreate,
    GroupResponse,
    GroupDetailResponse,
    GroupMemberAdd,
    GroupMemberResponse
)
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/groups", tags=["Groups"])


def verify_group_membership(group_id: int, user_id: int, db: Session) -> Group:
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    membership = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_id
    ).first()
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this group"
        )
    return group


@router.post("", response_model=GroupDetailResponse, status_code=status.HTTP_201_CREATED)
def create_group(
    group_in: GroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    group = Group(
        name=group_in.name,
        description=group_in.description,
        owner_id=current_user.id
    )
    db.add(group)
    db.commit()
    db.refresh(group)

    # Automatically add owner as first member
    member = GroupMember(group_id=group.id, user_id=current_user.id)
    db.add(member)
    db.commit()
    db.refresh(group)

    return group


@router.get("", response_model=List[GroupResponse])
def get_user_groups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Find all group IDs user belongs to
    memberships = db.query(GroupMember).filter(GroupMember.user_id == current_user.id).all()
    group_ids = [m.group_id for m in memberships]
    groups = db.query(Group).filter(Group.id.in_(group_ids)).all()
    return groups


@router.get("/{id}", response_model=GroupDetailResponse)
def get_group_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    group = verify_group_membership(id, current_user.id, db)
    return group


@router.post("/{id}/members", response_model=GroupMemberResponse, status_code=status.HTTP_201_CREATED)
def add_group_member(
    id: int,
    member_in: GroupMemberAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    group = verify_group_membership(id, current_user.id, db)

    # Find user to add by email
    target_user = db.query(User).filter(User.email == member_in.email).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{member_in.email}' not found"
        )

    # Check if already member
    existing = db.query(GroupMember).filter(
        GroupMember.group_id == group.id,
        GroupMember.user_id == target_user.id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this group"
        )

    new_member = GroupMember(group_id=group.id, user_id=target_user.id)
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member
