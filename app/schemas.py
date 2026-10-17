from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Kind = Literal["income", "expense"]
ExpenseGroup = Literal["fixed", "variable", "other"]
Status = Literal["paid", "pending"]
Priority = Literal["high", "medium", "low"]
PlanBase = Literal["forecast", "actual"]

Money = Annotated[float, Field(ge=0, le=1_000_000_000)]
NonEmpty = Annotated[str, Field(min_length=1)]


def _strip(value: str) -> str:
    return value.strip() if isinstance(value, str) else value


# ---------- Auth ----------
class Credentials(BaseModel):
    email: Annotated[str, Field(min_length=3, max_length=254)]
    password: Annotated[str, Field(min_length=6, max_length=128)]

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        value = value.strip().lower()
        local, _, domain = value.partition("@")
        if not local or "." not in domain:
            raise ValueError("Email inválido")
        return value


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str


# ---------- Lançamentos ----------
class TransactionIn(BaseModel):
    date: date
    description: Annotated[str, Field(min_length=1, max_length=120)]
    kind: Kind
    expense_group: ExpenseGroup | None = None
    category: Annotated[str, Field(min_length=1, max_length=60)]
    amount: Annotated[float, Field(gt=0, le=1_000_000_000)]
    status: Status = "paid"

    _strip_text = field_validator("description", "category", mode="before")(_strip)

    @model_validator(mode="after")
    def receita_sem_grupo(self) -> "TransactionIn":
        # Na planilha o Grupo só vale para despesas; para receitas é ignorado.
        if self.kind == "income":
            self.expense_group = None
        return self


class TransactionOut(TransactionIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------- Produtos ----------
class ProductIn(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=80)]
    category: Annotated[str, Field(max_length=60)] = ""
    price: Annotated[float, Field(gt=0, le=1_000_000_000)]
    priority: Priority = "medium"
    target_date: date | None = None
    saved: Money = 0

    _strip_text = field_validator("name", "category", mode="before")(_strip)


class ProductOut(ProductIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------- Config / Renda / Simulação ----------
class PlanSettingsIn(BaseModel):
    today_override: date | None = None
    plan_start: date
    plan_end: date
    days_soon: Annotated[int, Field(ge=0, le=365)] = 30
    tight_limit: Annotated[float, Field(gt=0, le=1)] = 0.7
    budget_income: Money = 0
    budget_fixed: Money = 0
    budget_variable: Money = 0
    budget_other: Money = 0
    plan_base: PlanBase = "forecast"
    scenarios: Annotated[list[Money], Field(min_length=1, max_length=8)]
    product_categories: list[NonEmpty]
    income_categories: Annotated[list[NonEmpty], Field(min_length=1)]
    expense_categories: Annotated[list[NonEmpty], Field(min_length=1)]

    @model_validator(mode="after")
    def check_window(self) -> "PlanSettingsIn":
        self.plan_start = self.plan_start.replace(day=1)
        if self.plan_end < self.plan_start:
            raise ValueError("O prazo final deve ser depois do primeiro mês do plano")
        return self


class PlanSettingsOut(PlanSettingsIn):
    model_config = ConfigDict(from_attributes=True)


# ---------- Importação ----------
class ImportIssue(BaseModel):
    sheet: str
    row: int
    message: str


class ImportReport(BaseModel):
    dry_run: bool
    transactions_new: int
    transactions_duplicated: int
    products_new: int
    products_duplicated: int
    settings_updated: bool
    errors: list[ImportIssue]
    warnings: list[ImportIssue]
