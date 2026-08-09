from typing import Dict, List, Optional
from pydantic import BaseModel


class CategoryBreakdownItem(BaseModel):
    category: str
    total_amount: float
    percentage: float
    count: int


class TopSpenderItem(BaseModel):
    user_id: int
    user_name: str
    total_spent: float


class MonthlyTrendItem(BaseModel):
    month: str
    total_amount: float


class GroupAnalyticsResponse(BaseModel):
    group_id: int
    total_expenses_count: int
    total_spent_amount: float
    average_expense_amount: float
    highest_spending_category: Optional[str]
    categories: List[CategoryBreakdownItem]
    top_spenders: List[TopSpenderItem]
    monthly_trends: List[MonthlyTrendItem]
