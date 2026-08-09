def test_group_creation_and_member_add(client):
    # Register Alice & Bob
    u1 = client.post("/auth/register", json={"email": "u1@example.com", "name": "User One", "password": "p"}).json()
    t1 = client.post("/auth/json-login", json={"email": "u1@example.com", "password": "p"}).json()["access_token"]

    u2 = client.post("/auth/register", json={"email": "u2@example.com", "name": "User Two", "password": "p"}).json()

    # Create Group
    headers = {"Authorization": f"Bearer {t1}"}
    g_res = client.post("/groups", json={"name": "Almaty Trip", "description": "Fun trip"}, headers=headers)
    assert g_res.status_code == 201
    group = g_res.json()
    assert group["name"] == "Almaty Trip"
    assert len(group["members"]) == 1

    # Add u2 to Group
    m_res = client.post(f"/groups/{group['id']}/members", json={"email": "u2@example.com"}, headers=headers)
    assert m_res.status_code == 201
    assert m_res.json()["user_id"] == u2["id"]

    # Verify group detail
    gd_res = client.get(f"/groups/{group['id']}", headers=headers)
    assert gd_res.status_code == 200
    assert len(gd_res.json()["members"]) == 2
