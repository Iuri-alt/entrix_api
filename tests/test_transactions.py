from tests.conftest import register_and_login

EXPENSE = {
    "date": "2019-03-15",
    "description": "Mercado",
    "kind": "expense",
    "expense_group": "variable",
    "category": "Alimentação",
    "amount": 120.5,
    "status": "pending",
}


def test_crud_keeps_date_including_past_years(client, auth):
    created = client.post("/transactions/", json=EXPENSE, headers=auth)
    assert created.status_code == 201
    item = created.json()
    assert item["date"] == "2019-03-15"

    updated = client.put(
        f"/transactions/{item['id']}", json={**EXPENSE, "amount": 99.9, "status": "paid"}, headers=auth
    ).json()
    assert updated["amount"] == 99.9 and updated["status"] == "paid"

    assert client.delete(f"/transactions/{item['id']}", headers=auth).status_code == 204
    assert client.get("/transactions/", headers=auth).json() == []


def test_income_drops_expense_group(client, auth):
    body = {**EXPENSE, "kind": "income", "category": "Salário", "expense_group": "fixed"}
    assert client.post("/transactions/", json=body, headers=auth).json()["expense_group"] is None


def test_filters_by_period(client, auth):
    for day in ("2026-09-30", "2026-10-01", "2026-10-31", "2026-11-01"):
        client.post("/transactions/", json={**EXPENSE, "date": day}, headers=auth)
    items = client.get("/transactions/?start=2026-10-01&end=2026-10-31", headers=auth).json()
    assert sorted(i["date"] for i in items) == ["2026-10-01", "2026-10-31"]


def test_validation_rejects_invalid_values(client, auth):
    for bad in ({"amount": 0}, {"amount": -5}, {"description": "  "}, {"kind": "outro"}):
        assert client.post("/transactions/", json={**EXPENSE, **bad}, headers=auth).status_code == 422


def test_users_are_isolated(client, auth):
    item = client.post("/transactions/", json=EXPENSE, headers=auth).json()
    other = register_and_login(client, "bia@example.com")
    assert client.get("/transactions/", headers=other).json() == []
    assert client.delete(f"/transactions/{item['id']}", headers=other).status_code == 404
    assert client.put(f"/transactions/{item['id']}", json=EXPENSE, headers=other).status_code == 404
