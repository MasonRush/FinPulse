from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models import AccountType, TransactionCategory

# Auth Schemas
class UserCreate(BaseModel):
    username: str
    password: str
    currency_preference: str = "USD"

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    currency_preference: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Account Schemas
class AccountCreate(BaseModel):
    type: AccountType
    institution_name: str
    balance: float = 0.0

class AccountUpdate(BaseModel):
    balance: float | None = None
    institution_name: str | None = None

class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    type: AccountType
    institution_name: str
    balance: float
    created_at: datetime

# Transaction Schemas
class TransactionCreate(BaseModel):
    account_id: int
    amount: float
    category: TransactionCategory
    description: Optional[str] = None
    timestamp: Optional[datetime] = None

class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    account_id: int
    amount: float
    category: TransactionCategory
    description: Optional[str]
    timestamp: datetime

# Portfolio Schemas
class PortfolioCreate(BaseModel):
    ticker_symbol: str
    shares_owned: float
    cost_basis: float

class PortfolioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    ticker_symbol: str
    shares_owned: float
    cost_basis: float
    created_at: datetime

# Dashboard Schemas
class DashboardSummary(BaseModel):
    net_worth: float
    total_assets: float
    total_liabilities: float
    monthly_income: float
    monthly_expenses: float
    savings_rate: float
    top_spending_categories: List[dict]

class InvestmentPerformance(BaseModel):
    total_value: float
    total_cost_basis: float
    total_return: float
    total_return_percentage: float
    time_weighted_return: float
    sharpe_ratio: Optional[float] = None
    asset_allocation: List[dict]

