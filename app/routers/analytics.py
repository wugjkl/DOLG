from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.analytics import GroupAnalyticsResponse
from app.core.dependencies import get_current_user
from app.routers.groups import verify_group_membership
from app.services.analytics_service import get_group_analytics

router = APIRouter(prefix="/groups/{group_id}", tags=["Analytics (Data Science)"])


@router.get("/analytics", response_model=GroupAnalyticsResponse)
def get_group_spending_analytics(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_group_membership(group_id, current_user.id, db)
    return get_group_analytics(db, group_id)
