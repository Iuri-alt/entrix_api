from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes import auth, plan_settings, products, spreadsheet, transactions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Entrix API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(transactions.router, prefix="/transactions", tags=["Lançamentos"])
app.include_router(products.router, prefix="/products", tags=["Produtos"])
app.include_router(plan_settings.router, prefix="/settings", tags=["Config"])
app.include_router(spreadsheet.router, prefix="/spreadsheet", tags=["Planilha"])


@app.get("/health", tags=["Infra"])
def health() -> dict[str, str]:
    return {"status": "ok"}
