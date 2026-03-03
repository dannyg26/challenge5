from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from ..db import get_db
from ..deps import get_current_user
from .. import models, schemas

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("", response_model=schemas.DashboardOut)
def dashboard(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    txs = db.query(models.Transaction).filter(models.Transaction.user_id == user.id).all()
    balance = sum(t.amount for t in txs)

    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)
    month_txs = [t for t in txs if t.timestamp >= month_start]
    income = sum(t.amount for t in month_txs if t.amount > 0)
    expenses = sum(-t.amount for t in month_txs if t.amount < 0)

    return {
        "balance_estimate": float(balance),
        "month_income": float(income),
        "month_expenses": float(expenses),
        "net_this_month": float(income - expenses),
    }
