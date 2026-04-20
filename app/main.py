from fastapi import FastAPI
from app.database import Base, engine
from app.routes import  auth, expenses

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Entrix API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])