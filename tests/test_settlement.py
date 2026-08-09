def test_greedy_settle_up_algorithm(client):
    # Register 4 users: Alice, Bob, Charlie, David
    def reg(email, name):
        client.post("/auth/register", json={"email": email, "name": name, "password": "pass"})
        return client.post("/auth/json-login", json={"email": email, "password": "pass"}).json()

    a_auth = reg("a@debt.com", "Alice")
    b_auth = reg("b@debt.com", "Bob")
    c_auth = reg("c@debt.com", "Charlie")
    d_auth = reg("d@debt.com", "David")

    h_a = {"Authorization": f"Bearer {a_auth['access_token']}"}
    h_b = {"Authorization": f"Bearer {b_auth['access_token']}"}

    # Alice creates group and adds Bob, Charlie, David
    g = client.post("/groups", json={"name": "Greedy Test Group"}, headers=h_a).json()
    for e in ["b@debt.com", "c@debt.com", "d@debt.com"]:
        client.post(f"/groups/{g['id']}/members", json={"email": e}, headers=h_a)

    # Alice pays 400 (each owes 100) -> Alice net = +300, others = -100
    client.post(
        f"/groups/{g['id']}/expenses",
        json={"amount": 400.0, "description": "Resort", "split_type": "equal"},
        headers=h_a
    )

    # Check Settle Up Suggestions
    su_res = client.get(f"/groups/{g['id']}/settle-up", headers=h_a)
    assert su_res.status_code == 200
    plan = su_res.json()
    assert len(plan) == 3  # 3 transactions: Bob -> Alice, Charlie -> Alice, David -> Alice

    for item in plan:
        assert item["to_user_id"] == a_auth["user"]["id"]
        assert item["amount"] == 100.0

    # Bob records payment of 100 to Alice
    settle_res = client.post(
        f"/groups/{g['id']}/settlements",
        json={"payee_id": a_auth["user"]["id"], "amount": 100.0},
        headers=h_b
    )
    assert settle_res.status_code == 201

    # Re-check settle up: Bob should no longer be in transactions list
    new_plan = client.get(f"/groups/{g['id']}/settle-up", headers=h_a).json()
    assert len(new_plan) == 2
    from_uids = [tx["from_user_id"] for tx in new_plan]
    assert b_auth["user"]["id"] not in from_uids
