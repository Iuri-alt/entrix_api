from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔥 CREATE
@router.post("/", response_model=schemas.ExpenseOut)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = models.Expense(
        title=expense.title,
        amount=expense.value,
        category="income" if expense.isIncome else "expense",
        user_id=1
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return schemas.ExpenseOut(
        id=new_expense.id,
        title=new_expense.title,
        value=new_expense.amount,
        isIncome=new_expense.category == "income",
        date=new_expense.date,
    )

# 🔥 LIST
@router.get("/", response_model=List[schemas.ExpenseOut])
def list_expenses(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()

    return [
        schemas.ExpenseOut(
            id=e.id,
            title=e.title,
            value=e.amount,
            isIncome=e.category == "income",
            date=e.date,
        )
        for e in expenses
    ]

# 🗑️ DELETE
@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    exp = db.query(models.Expense).filter(models.Expense.id == expense_id).first()

    if exp:
        db.delete(exp)
        db.commit()

    return {"msg": "deletado"}
