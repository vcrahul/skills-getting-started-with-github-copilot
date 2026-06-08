def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # ensure at least one known activity exists
    assert "Chess Club" in data


def test_signup_and_duplicate(client):
    activity = "Tennis Club"
    email = "tester@example.com"

    # initial count
    resp = client.get("/activities")
    initial_count = len(resp.json()[activity]["participants"])

    # first signup should succeed
    resp = client.post(
        f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    resp = client.get("/activities")
    assert len(resp.json()[activity]["participants"]) == initial_count + 1

    # duplicate signup should be rejected
    resp = client.post(
        f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 400


def test_unregister(client):
    activity = "Basketball Team"
    email = "removeme@example.com"

    # sign up then remove
    resp = client.post(
        f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200

    resp = client.delete(
        f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200

    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email.lower() not in [p.lower() for p in participants]
