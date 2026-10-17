import os
import secrets
import warnings
from dataclasses import dataclass


def _database_url() -> str:
    url = os.getenv("DATABASE_URL", "sqlite:///./entrix.db")
    # Render/Heroku entregam "postgres://"; o SQLAlchemy 2 exige o driver explícito.
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


def _secret_key() -> str:
    key = os.getenv("SECRET_KEY")
    if key:
        return key
    warnings.warn(
        "SECRET_KEY não definida: usando chave temporária. "
        "Todos os tokens serão invalidados a cada reinício.",
        stacklevel=2,
    )
    return secrets.token_urlsafe(48)


@dataclass(frozen=True)
class Settings:
    database_url: str
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_days: int = int(os.getenv("ACCESS_TOKEN_DAYS", "30"))


settings = Settings(database_url=_database_url(), secret_key=_secret_key())
