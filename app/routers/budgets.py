from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user
from .. import models, schemas

router = APIRouter(prefix="/budgets", tags=["budgets"])

@router.get("", response_model=list[schemas.BudgetOut])
def list_budgets(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Budget).filter(models.Budget.user_id == user.id).order_by(models.Budget.category.asc()).all()

@router.post("", response_model=schemas.BudgetOut)
def upsert_budget(payload: schemas.BudgetUpsert, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    cat = payload.category.strip().lower()
    b = db.query(models.Budget).filter(models.Budget.user_id == user.id, models.Budget.category == cat).first()
    if b:
        b.monthly_limit = payload.monthly_limit
        b.active = payload.active
    else:
        b = models.Budget(user_id=user.id, category=cat, monthly_limit=payload.monthly_limit, active=payload.active)
        db.add(b)
    db.commit()
    db.refresh(b)
    return b

@router.delete("/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    b = db.query(models.Budget).filter(models.Budget.id == budget_id, models.Budget.user_id == user.id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Budget not found")
    db.delete(b)
    db.commit()
    return {"ok": True}
