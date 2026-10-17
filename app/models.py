from datetime import date, datetime, timezone

from sqlalchemy import JSON, Date, DateTime, Float, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    # Guarda o hash bcrypt. Linhas antigas em texto puro são convertidas no login.
    password: Mapped[str] = mapped_column(String)

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    products: Mapped[list["Product"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    plan_settings: Mapped["PlanSettings | None"] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )


class Transaction(TimestampMixin, Base):
    """Linha da aba Lançamentos."""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    description: Mapped[str] = mapped_column(String(120))
    kind: Mapped[str] = mapped_column(String(10))  # income | expense
    expense_group: Mapped[str | None] = mapped_column(String(10), nullable=True)
    category: Mapped[str] = mapped_column(String(60))
    amount: Mapped[float] = mapped_column(Numeric(12, 2, asdecimal=False))
    status: Mapped[str] = mapped_column(String(10), default="paid")  # paid | pending

    user: Mapped[User] = relationship(back_populates="transactions")


class Product(TimestampMixin, Base):
    """Linha da aba Produtos."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(80))
    category: Mapped[str] = mapped_column(String(60), default="")
    price: Mapped[float] = mapped_column(Numeric(12, 2, asdecimal=False))
    priority: Mapped[str] = mapped_column(String(10), default="medium")  # high|medium|low
    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    saved: Mapped[float] = mapped_column(Numeric(12, 2, asdecimal=False), default=0)

    user: Mapped[User] = relationship(back_populates="products")


class PlanSettings(TimestampMixin, Base):
    """Abas Config, Renda e Simulação (uma linha por usuário)."""

    __tablename__ = "plan_settings"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    today_override: Mapped[date | None] = mapped_column(Date, nullable=True)
    plan_start: Mapped[date] = mapped_column(Date)
    plan_end: Mapped[date] = mapped_column(Date)
    days_soon: Mapped[int] = mapped_column(Integer, default=30)
    tight_limit: Mapped[float] = mapped_column(Float, default=0.7)
    budget_income: Mapped[float] = mapped_column(Float, default=0)
    budget_fixed: Mapped[float] = mapped_column(Float, default=0)
    budget_variable: Mapped[float] = mapped_column(Float, default=0)
    budget_other: Mapped[float] = mapped_column(Float, default=0)
    plan_base: Mapped[str] = mapped_column(String(10), default="forecast")  # forecast|actual
    scenarios: Mapped[list[float]] = mapped_column(JSON)
    product_categories: Mapped[list[str]] = mapped_column(JSON)
    income_categories: Mapped[list[str]] = mapped_column(JSON)
    expense_categories: Mapped[list[str]] = mapped_column(JSON)

    user: Mapped[User] = relationship(back_populates="plan_settings")
