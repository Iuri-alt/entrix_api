from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.models import Product, User
from app.schemas import ProductIn, ProductOut

router = APIRouter()


def _owned(db: Session, user: User, product_id: int) -> Product:
    item = db.get(Product, product_id)
    if item is None or item.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto não encontrado")
    return item


@router.get("/", response_model=list[ProductOut])
def list_products(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[Product]:
    query = select(Product).where(Product.user_id == user.id).order_by(Product.id)
    return list(db.scalars(query))


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    body: ProductIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Product:
    item = Product(user_id=user.id, **body.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    body: ProductIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Product:
    item = _owned(db, user, product_id)
    for field, value in body.model_dump().items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Response:
    db.delete(_owned(db, user, product_id))
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
