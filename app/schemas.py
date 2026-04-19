from pydantic import BaseModel
from datetime import datetime

# 🔐 USER
class UserCreate(BaseModel):
    email: str
    password: str


# 💰 EXPENSE (entrada do Flutter)
class ExpenseCreate(BaseModel):
    title: str
    value: float
    isIncome: bool


# 📤 EXPENSE (resposta pro Flutter)
class ExpenseOut(BaseModel):
    id: int
    title: str
    value: float
    isIncome: bool
    date: datetime

    class Config:
        from_attributes = True
