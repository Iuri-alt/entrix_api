"""Posições das células na planilha Controle_Financeiro (fonte de verdade do layout)."""

FIRST_DATA_ROW = 6

SHEET_TRANSACTIONS = "Lançamentos"
SHEET_PRODUCTS = "Produtos"
SHEET_CONFIG = "Config"
SHEET_INCOME = "Renda"
SHEET_SIMULATION = "Simulação"

TRANSACTION_HEADERS = [
    "Data", "Descrição", "Tipo", "Grupo da despesa", "Categoria", "Valor", "Situação",
]
PRODUCT_HEADERS = ["Produto", "Categoria", "Preço", "Prioridade", "Data desejada", "Já tenho guardado"]

KIND_LABELS = {"income": "Receita", "expense": "Despesa"}
GROUP_LABELS = {"fixed": "Fixa", "variable": "Variável", "other": "Outro compromisso"}
STATUS_LABELS = {"paid": "Pago", "pending": "Pendente"}
PRIORITY_LABELS = {"high": "Alta", "medium": "Média", "low": "Baixa"}
BASE_LABELS = {"forecast": "Previsto", "actual": "Realizado"}


def invert(labels: dict[str, str]) -> dict[str, str]:
    return {label.casefold(): code for code, label in labels.items()}


# Config
CONFIG_PLAN_START = "B5"
CONFIG_PLAN_END = "B6"
CONFIG_DAYS_SOON = "B7"
CONFIG_TIGHT_LIMIT = "B8"
CONFIG_PRODUCT_CATEGORIES_COL = "H"
CONFIG_TRANSACTION_CATEGORIES_COL = "J"
CONFIG_LIST_FIRST_ROW = 4
# As 3 primeiras categorias dos lançamentos (J4:J6) são de receita (nota da aba Config).
INCOME_CATEGORY_COUNT = 3

# Renda
INCOME_BUDGET_CELLS = {
    "budget_income": "B5",
    "budget_fixed": "B6",
    "budget_variable": "B7",
    "budget_other": "B8",
}
INCOME_PLAN_BASE = "B11"

# Simulação
SIMULATION_SCENARIO_CELLS = ["B5", "C5", "D5", "E5"]
