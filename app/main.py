from fastapi import FastAPI
from app.database import Base, engine
from app.routes import  auth, expenses, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Entrix API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])