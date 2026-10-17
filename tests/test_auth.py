from sqlalchemy import select

from app.database import SessionLocal
from app.models import User


def test_register_hashes_password(client):
    response = client.post("/auth/register", json={"email": "Ana@Example.com ", "password": "segredo123"})
    assert response.status_code == 201
    assert response.json()["email"] == "ana@example.com"
    with SessionLocal() as db:
        stored = db.scalar(select(User.password))
    assert stored.startswith("$2") and stored != "segredo123"


def test_register_duplicate_returns_409(client):
    body = {"email": "ana@example.com", "password": "segredo123"}
    client.post("/auth/register", json=body)
    assert client.post("/auth/register", json=body).status_code == 409


def test_login_wrong_password_returns_401(client):
    client.post("/auth/register", json={"email": "ana@example.com", "password": "segredo123"})
    response = client.post("/auth/login", json={"email": "ana@example.com", "password": "errada123"})
    assert response.status_code == 401


def test_legacy_plaintext_password_is_upgraded_on_login(client):
    with SessionLocal() as db:
        db.add(User(email="velho@example.com", password="antiga123"))
        db.commit()
    response = client.post("/auth/login", json={"email": "velho@example.com", "password": "antiga123"})
    assert response.status_code == 200
    with SessionLocal() as db:
        assert db.scalar(select(User.password)).startswith("$2")


def test_protected_routes_require_token(client):
    for path in ("/transactions/", "/products/", "/settings/", "/auth/me"):
        assert client.get(path).status_code == 401
    assert client.get("/transactions/", headers={"Authorization": "Bearer lixo"}).status_code == 401
