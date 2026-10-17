PRODUCT = {
    "name": "Korg Kronos 2",
    "category": "Música",
    "price": 6000,
    "priority": "medium",
    "target_date": "2027-01-10",
    "saved": 110,
}


def test_product_crud(client, auth):
    item = client.post("/products/", json=PRODUCT, headers=auth).json()
    assert item["saved"] == 110
    updated = client.put(f"/products/{item['id']}", json={**PRODUCT, "saved": 500}, headers=auth).json()
    assert updated["saved"] == 500
    assert client.delete(f"/products/{item['id']}", headers=auth).status_code == 204
    assert client.get("/products/", headers=auth).json() == []


def test_product_without_date_is_allowed(client, auth):
    body = {**PRODUCT, "target_date": None}
    assert client.post("/products/", json=body, headers=auth).status_code == 201


def test_settings_defaults_match_spreadsheet(client, auth):
    data = client.get("/settings/", headers=auth).json()
    assert data["days_soon"] == 30
    assert data["tight_limit"] == 0.7
    assert data["scenarios"] == [300, 500, 700, 1000]
    assert data["income_categories"] == ["Salário", "Renda extra", "Outras receitas"]
    assert len(data["expense_categories"]) == 15


def test_settings_update_has_no_month_cap(client, auth):
    data = client.get("/settings/", headers=auth).json()
    data.update(plan_start="2026-10-15", plan_end="2031-12-31")
    saved = client.put("/settings/", json=data, headers=auth).json()
    assert saved["plan_start"] == "2026-10-01"
    assert saved["plan_end"] == "2031-12-31"


def test_settings_rejects_inverted_window(client, auth):
    data = client.get("/settings/", headers=auth).json()
    data.update(plan_start="2027-10-01", plan_end="2026-01-01")
    assert client.put("/settings/", json=data, headers=auth).status_code == 422
