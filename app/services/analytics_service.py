import pandas as pd
from typing import List
from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.models.user import User
from app.schemas.analytics import (
    GroupAnalyticsResponse,
    CategoryBreakdownItem,
    TopSpenderItem,
    MonthlyTrendItem
)


def get_group_analytics(db: Session, group_id: int) -> GroupAnalyticsResponse:
    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()
    
    if not expenses:
        return GroupAnalyticsResponse(
            group_id=group_id,
            total_expenses_count=0,
            total_spent_amount=0.0,
            average_expense_amount=0.0,
            highest_spending_category=None,
            categories=[],
            top_spenders=[],
            monthly_trends=[]
        )

    # Convert expenses to pandas DataFrame
    data = []
    for exp in expenses:
        data.append({
            "id": exp.id,
            "paid_by": exp.paid_by,
            "amount": exp.amount,
            "category": exp.category,
            "created_at": exp.created_at
        })

    df = pd.DataFrame(data)

    total_count = len(df)
    total_spent = float(df["amount"].sum())
    avg_expense = float(df["amount"].mean())

    # 1. Category Breakdown
    cat_df = df.groupby("category")["amount"].agg(["sum", "count"]).reset_index()
    cat_df["percentage"] = (cat_df["sum"] / total_spent * 100).round(2)
    
    category_items = []
    for _, row in cat_df.iterrows():
        category_items.append(
            CategoryBreakdownItem(
                category=str(row["category"]),
                total_amount=round(float(row["sum"]), 2),
                percentage=float(row["percentage"]),
                count=int(row["count"])
            )
        )
    category_items.sort(key=lambda x: x.total_amount, reverse=True)
    highest_cat = category_items[0].category if category_items else None

    # 2. Top Spenders
    user_ids = df["paid_by"].unique().tolist()
    users_dict = {u.id: u.name for u in db.query(User).filter(User.id.in_(user_ids)).all()}
    
    spender_df = df.groupby("paid_by")["amount"].sum().reset_index()
    spender_df.sort_values(by="amount", ascending=False, inplace=True)

    top_spenders = []
    for _, row in spender_df.iterrows():
        uid = int(row["paid_by"])
        top_spenders.append(
            TopSpenderItem(
                user_id=uid,
                user_name=users_dict.get(uid, f"User #{uid}"),
                total_spent=round(float(row["amount"]), 2)
            )
        )

    # 3. Monthly Trends
    df["month"] = df["created_at"].dt.strftime("%Y-%m")
    trend_df = df.groupby("month")["amount"].sum().reset_index().sort_values(by="month")
    
    monthly_trends = []
    for _, row in trend_df.iterrows():
        monthly_trends.append(
            MonthlyTrendItem(
                month=str(row["month"]),
                total_amount=round(float(row["amount"]), 2)
            )
        )

    return GroupAnalyticsResponse(
        group_id=group_id,
        total_expenses_count=total_count,
        total_spent_amount=round(total_spent, 2),
        average_expense_amount=round(avg_expense, 2),
        highest_spending_category=highest_cat,
        categories=category_items,
        top_spenders=top_spenders,
        monthly_trends=monthly_trends
    )
