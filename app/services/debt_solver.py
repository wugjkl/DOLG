from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.group import Group, GroupMember
from app.models.expense import Expense, ExpenseShare
from app.models.settlement import Settlement
from app.models.user import User
from app.schemas.balance import MemberBalanceItem, GroupBalanceResponse, TransactionSuggestion


def calculate_group_balances(db: Session, group_id: int) -> GroupBalanceResponse:
    # 1. Fetch group members
    group_memberships = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
    user_ids = [m.user_id for m in group_memberships]
    users_dict: Dict[int, User] = {u.id: u for u in db.query(User).filter(User.id.in_(user_ids)).all()}

    # Initialize data maps
    paid_map = {uid: 0.0 for uid in user_ids}
    owed_map = {uid: 0.0 for uid in user_ids}
    settlements_paid_map = {uid: 0.0 for uid in user_ids}
    settlements_received_map = {uid: 0.0 for uid in user_ids}

    # 2. Accumulate expenses
    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()
    total_spending = 0.0
    for exp in expenses:
        total_spending += exp.amount
        if exp.paid_by in paid_map:
            paid_map[exp.paid_by] += exp.amount
        
        # Shares
        for share in exp.shares:
            if share.user_id in owed_map:
                owed_map[share.user_id] += share.share_amount

    # 3. Accumulate settlements
    settlements = db.query(Settlement).filter(Settlement.group_id == group_id).all()
    for s in settlements:
        if s.payer_id in settlements_paid_map:
            settlements_paid_map[s.payer_id] += s.amount
        if s.payee_id in settlements_received_map:
            settlements_received_map[s.payee_id] += s.amount

    # 4. Construct MemberBalanceItem list
    member_balances: List[MemberBalanceItem] = []
    for uid in user_ids:
        user = users_dict.get(uid)
        paid = round(paid_map[uid], 2)
        owed = round(owed_map[uid], 2)
        s_paid = round(settlements_paid_map[uid], 2)
        s_rec = round(settlements_received_map[uid], 2)
        
        # Net balance calculation:
        # positive (+) means user is owed money (creditor)
        # negative (-) means user owes money (debtor)
        net = round(paid - owed + s_paid - s_rec, 2)
        
        member_balances.append(
            MemberBalanceItem(
                user_id=uid,
                user_name=user.name if user else f"User #{uid}",
                user_email=user.email if user else "",
                paid_total=paid,
                owed_total=owed,
                settlements_paid=s_paid,
                settlements_received=s_rec,
                net_balance=net
            )
        )

    return GroupBalanceResponse(
        group_id=group_id,
        total_group_spending=round(total_spending, 2),
        members=member_balances
    )


def solve_greedy_debt_minimization(balances: GroupBalanceResponse) -> List[TransactionSuggestion]:
    """
    Greedy Debt Minimization Algorithm:
    - Matches highest debtor with highest creditor to eliminate debts in minimum possible transactions.
    - Time Complexity: O(N log N) where N is the number of group members.
    """
    debtors = []   # list of [amount_owed, user_id, user_name]
    creditors = [] # list of [amount_to_receive, user_id, user_name]

    for member in balances.members:
        net = member.net_balance
        if net < -0.005:
            debtors.append([-net, member.user_id, member.user_name])
        elif net > 0.005:
            creditors.append([net, member.user_id, member.user_name])

    transactions: List[TransactionSuggestion] = []

    while debtors and creditors:
        # Sort so largest amounts are processed first (Greedy choice)
        debtors.sort(key=lambda x: x[0], reverse=True)
        creditors.sort(key=lambda x: x[0], reverse=True)

        debtor = debtors[0]
        creditor = creditors[0]

        settlement_amount = min(debtor[0], creditor[0])
        settlement_amount = round(settlement_amount, 2)

        if settlement_amount > 0:
            transactions.append(
                TransactionSuggestion(
                    from_user_id=debtor[1],
                    from_user_name=debtor[2],
                    to_user_id=creditor[1],
                    to_user_name=creditor[2],
                    amount=settlement_amount
                )
            )

        debtor[0] -= settlement_amount
        creditor[0] -= settlement_amount

        if debtor[0] < 0.005:
            debtors.pop(0)
        if creditor[0] < 0.005:
            creditors.pop(0)

    return transactions
