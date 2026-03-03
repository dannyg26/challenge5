from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user
from .. import models, schemas
from ..utils import mortgage_amortization_summary

router = APIRouter(prefix="/mortgage", tags=["mortgage"])

@router.get("", response_model=schemas.MortgageOut | None)
def get_mortgage(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    m = db.query(models.Mortgage).filter(models.Mortgage.user_id == user.id).first()
    if not m:
        return None
    return {"principal": m.principal, "annual_rate": m.annual_rate, "term_months": m.term_months, "extra_payment": m.extra_payment}

@router.post("", response_model=schemas.MortgageOut)
def upsert_mortgage(payload: schemas.MortgageUpsert, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    m = db.query(models.Mortgage).filter(models.Mortgage.user_id == user.id).first()
    if not m:
        m = models.Mortgage(user_id=user.id, principal=payload.principal, annual_rate=payload.annual_rate, term_months=payload.term_months, extra_payment=payload.extra_payment)
        db.add(m)
    else:
        m.principal = payload.principal
        m.annual_rate = payload.annual_rate
        m.term_months = payload.term_months
        m.extra_payment = payload.extra_payment
    db.commit()
    return {"principal": m.principal, "annual_rate": m.annual_rate, "term_months": m.term_months, "extra_payment": m.extra_payment}

@router.get("/summary")
def mortgage_summary(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    m = db.query(models.Mortgage).filter(models.Mortgage.user_id == user.id).first()
    if not m:
        return {"monthly_payment": 0.0, "months_to_payoff": 0, "total_interest": 0.0}
    return mortgage_amortization_summary(m.principal, m.annual_rate, m.term_months, m.extra_payment)
