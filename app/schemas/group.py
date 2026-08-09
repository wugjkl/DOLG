from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.user import UserResponse


class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None


class GroupMemberAdd(BaseModel):
    email: str


class GroupMemberResponse(BaseModel):
    id: int
    user_id: int
    user: UserResponse
    joined_at: datetime

    class Config:
        from_attributes = True


class GroupResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class GroupDetailResponse(GroupResponse):
    owner: UserResponse
    members: List[GroupMemberResponse] = []
