def test_expense_splitting_equal_and_exact(client):
    # Setup 3 Users: Alice, Bob, Charlie
    t1 = client.post("/auth/json-login", json={"email": "alice@ex.com", "password": "p"}).json() if False else None
    
    # Register 3 users
    u1 = client.post("/auth/register", json={"email": "a@ex.com", "name": "Alice", "password": "p"}).json()
    t1 = client.post("/auth/json-login", json={"email": "a@ex.com", "password": "p"}).json()["access_token"]
    h1 = {"Authorization": f"Bearer {t1}"}

    u2 = client.post("/auth/register", json={"email": "b@ex.com", "name": "Bob", "password": "p"}).json()
    u3 = client.post("/auth/register", json={"email": "c@ex.com", "name": "Charlie", "password": "p"}).json()

    # Create Group & Add members
    g = client.post("/groups", json={"name": "Dinner Group"}, headers=h1).json()
    client.post(f"/groups/{g['id']}/members", json={"email": "b@ex.com"}, headers=h1)
    client.post(f"/groups/{g['id']}/members", json={"email": "c@ex.com"}, headers=h1)

    # 1. Equal Expense: Alice pays 300
    e1 = client.post(
        f"/groups/{g['id']}/expenses",
        json={
            "amount": 300.0,
            "description": "Dinner",
            "category": "Food & Drinks",
            "split_type": "equal"
        },
        headers=h1
    )
    assert e1.status_code == 201
    shares = e1.json()["shares"]
    assert len(shares) == 3
    for s in shares:
        assert s["share_amount"] == 100.0

    # 2. Check Balance
    bal_res = client.get(f"/groups/{g['id']}/balance", headers=h1)
    assert bal_res.status_code == 200
    b_data = bal_res.json()
    
    # Alice paid 300, owes 100 -> net = +200
    # Bob paid 0, owes 100 -> net = -100
    # Charlie paid 0, owes 100 -> net = -100
    for m in b_data["members"]:
        if m["user_id"] == u1["id"]:
            assert m["net_balance"] == 200.0
        else:
            assert m["net_balance"] == -100.0
