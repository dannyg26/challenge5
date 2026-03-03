from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TransactionCreate(BaseModel):
    amount: float
    category: str = "general"
    description: str = ""

class TransactionOut(BaseModel):
    id: int
    timestamp: datetime
    amount: float
    category: str
    description: str
    class Config:
        from_attributes = True

class InvestmentCreate(BaseModel):
    ticker: str
    shares: float = 0.0
    avg_cost: float = 0.0
    notes: str = ""

class InvestmentOut(BaseModel):
    id: int
    ticker: str
    shares: float
    avg_cost: float
    notes: str
    class Config:
        from_attributes = True

class MortgageUpsert(BaseModel):
    principal: float
    annual_rate: float
    term_months: int
    extra_payment: float = 0.0

class MortgageOut(BaseModel):
    principal: float
    annual_rate: float
    term_months: int
    extra_payment: float

class BudgetUpsert(BaseModel):
    category: str
    monthly_limit: float
    active: bool = True

class BudgetOut(BaseModel):
    id: int
    category: str
    monthly_limit: float
    active: bool
    class Config:
        from_attributes = True

class DashboardOut(BaseModel):
    balance_estimate: float
    month_income: float
    month_expenses: float
    net_this_month: float
