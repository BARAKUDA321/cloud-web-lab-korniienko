from app import app


def test_index():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "running"


def test_admin_stats_requires_token():
    client = app.test_client()
    response = client.get("/api/admin/stats")

    assert response.status_code == 401


def test_create_lesson_requires_token():
    client = app.test_client()
    response = client.post(
        "/api/lessons",
        json={"subject": "Test", "room": "ауд. 1", "status": "new"}
    )

    assert response.status_code == 401
