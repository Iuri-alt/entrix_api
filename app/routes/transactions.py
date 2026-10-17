from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.models import Transaction, User
from app.schemas import TransactionIn, TransactionOut

router = APIRouter()


def _owned(db: Session, user: User, transaction_id: int) -> Transaction:
    item = db.get(Transaction, transaction_id)
    if item is None or item.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Lançamento não encontrado")
    return item


@router.get("/", response_model=list[TransactionOut])
def list_transactions(
    start: date | None = Query(None, description="Data inicial (inclusive)"),
    end: date | None = Query(None, description="Data final (inclusive)"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Transaction]:
    query = select(Transaction).where(Transaction.user_id == user.id)
    if start:
        query = query.where(Transaction.date >= start)
    if end:
        query = query.where(Transaction.date <= end)
    return list(db.scalars(query.order_by(Transaction.date.desc(), Transaction.id.desc())))


@router.post("/", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(
    body: TransactionIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Transaction:
    item = Transaction(user_id=user.id, **body.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{transaction_id}", response_model=TransactionOut)
def update_transaction(
    transaction_id: int,
    body: TransactionIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Transaction:
    item = _owned(db, user, transaction_id)
    for field, value in body.model_dump().items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    db.delete(_owned(db, user, transaction_id))
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
