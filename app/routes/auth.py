from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from app.auth import create_token

router = APIRouter()

# 🔌 DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🧾 REGISTER
@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    new_user = models.User(
        email=user.email,
        password=user.password  # depois a gente melhora com hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "usuário criado com sucesso"}

# 🔐 LOGIN
@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(
            status_code=401,
            detail="credenciais inválidas"
        )

    token = create_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
