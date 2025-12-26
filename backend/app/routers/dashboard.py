from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app.database import get_db
from app.models import User, Account, Transaction, AccountType, TransactionCategory
from app.schemas import DashboardSummary
from app.security import get_current_user

router = APIRouter()

@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get all accounts for the user
    accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    
    # Calculate total assets and liabilities
    total_assets = sum(
        acc.balance for acc in accounts 
        if acc.type in [AccountType.CHECKING, AccountType.SAVINGS, AccountType.BROKERAGE]
    )
    total_liabilities = sum(
        acc.balance for acc in accounts 
        if acc.type == AccountType.LOAN
    )
    net_worth = total_assets - total_liabilities
    
    # Calculate monthly income and expenses (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    monthly_income_result = db.query(func.sum(Transaction.amount)).join(Account).filter(
        Account.user_id == current_user.id,
        Transaction.category == TransactionCategory.SALARY,
        Transaction.timestamp >= thirty_days_ago
    ).scalar() or 0.0
    
    monthly_expenses_result = db.query(func.sum(Transaction.amount)).join(Account).filter(
        Account.user_id == current_user.id,
        Transaction.category != TransactionCategory.SALARY,
        Transaction.amount < 0,
        Transaction.timestamp >= thirty_days_ago
    ).scalar() or 0.0
    
    monthly_income = abs(monthly_income_result)
    monthly_expenses = abs(monthly_expenses_result)
    
    # Calculate savings rate
    if monthly_income > 0:
        savings_rate = 1 - (monthly_expenses / monthly_income)
    else:
        savings_rate = 0.0
    
    # Get top spending categories
    category_totals = db.query(
        Transaction.category,
        func.sum(func.abs(Transaction.amount)).label("total")
    ).join(Account).filter(
        Account.user_id == current_user.id,
        Transaction.category != TransactionCategory.SALARY,
        Transaction.amount < 0,
        Transaction.timestamp >= thirty_days_ago
    ).group_by(Transaction.category).order_by(func.sum(func.abs(Transaction.amount)).desc()).limit(5).all()
    
    top_spending_categories = [
        {"category": cat.value, "amount": float(total)}
        for cat, total in category_totals
    ]
    
    return DashboardSummary(
        net_worth=net_worth,
        total_assets=total_assets,
        total_liabilities=total_liabilities,
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        savings_rate=savings_rate,
        top_spending_categories=top_spending_categories
    )

