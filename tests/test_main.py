from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

auth = ("admin", "admin123")


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "docs" in resp.json()


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_create_todo():
    resp = client.post("/todos", json={"title": "Test"}, auth=auth)
    assert resp.status_code == 201
    assert resp.json()["title"] == "Test"
    return resp.json()["id"]


def test_list_todos():
    client.post("/todos", json={"title": "Test2"}, auth=auth)
    resp = client.get("/todos", auth=auth)
    assert resp.status_code == 200
    assert len(resp.json()) >= 2


def test_get_todo():
    tid = test_create_todo()
    resp = client.get(f"/todos/{tid}", auth=auth)
    assert resp.status_code == 200
    assert resp.json()["id"] == tid


def test_update_todo():
    tid = test_create_todo()
    resp = client.put(f"/todos/{tid}", json={"completed": True}, auth=auth)
    assert resp.status_code == 200
    assert resp.json()["completed"] is True


def test_delete_todo():
    tid = test_create_todo()
    resp = client.delete(f"/todos/{tid}", auth=auth)
    assert resp.status_code == 204


def test_unauthorized():
    resp = client.get("/todos")
    assert resp.status_code == 401


def test_filter_completed():
    resp = client.get("/todos?completed=true", auth=auth)
    assert resp.status_code == 200
    for t in resp.json():
        assert t["completed"] is True


def test_404():
    resp = client.get("/todos/99999", auth=auth)
    assert resp.status_code == 404
