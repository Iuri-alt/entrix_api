"""Valores padrão herdados da aba Config da planilha original."""

from datetime import date

PRODUCT_CATEGORIES = [
    "Eletrônicos", "Computador", "Casa", "Estudos", "Lazer",
    "Música", "Saúde", "Transporte", "Vestuário", "Outros",
]
INCOME_CATEGORIES = ["Salário", "Renda extra", "Outras receitas"]
EXPENSE_CATEGORIES = [
    "Moradia", "Alimentação", "Transporte", "Saúde", "Educação", "Lazer",
    "Assinaturas", "Vestuário", "Cartão/Dívidas", "Presentes e doações",
    "Impostos e taxas", "Pets", "Viagens", "Cuidados pessoais", "Outros",
]
SCENARIOS = [300.0, 500.0, 700.0, 1000.0]
DAYS_SOON = 30
TIGHT_LIMIT = 0.7


def default_plan_window(today: date) -> tuple[date, date]:
    """Do mês atual até o fim do ano seguinte."""
    return date(today.year, today.month, 1), date(today.year + 1, 12, 31)
