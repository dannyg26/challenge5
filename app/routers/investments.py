from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user
from .. import models, schemas

router = APIRouter(prefix="/investments", tags=["investments"])

@router.get("", response_model=list[schemas.InvestmentOut])
def list_investments(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Investment).filter(models.Investment.user_id == user.id).order_by(models.Investment.ticker.asc()).all()

@router.post("", response_model=schemas.InvestmentOut)
def upsert_investment(payload: schemas.InvestmentCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    ticker = payload.ticker.upper().strip()
    inv = db.query(models.Investment).filter(models.Investment.user_id == user.id, models.Investment.ticker == ticker).first()
    if inv:
        inv.shares = payload.shares
        inv.avg_cost = payload.avg_cost
        inv.notes = payload.notes
    else:
        inv = models.Investment(user_id=user.id, ticker=ticker, shares=payload.shares, avg_cost=payload.avg_cost, notes=payload.notes)
        db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv

@router.delete("/{inv_id}")
def delete_investment(inv_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    inv = db.query(models.Investment).filter(models.Investment.id == inv_id, models.Investment.user_id == user.id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investment not found")
    db.delete(inv)
    db.commit()
    return {"ok": True}
