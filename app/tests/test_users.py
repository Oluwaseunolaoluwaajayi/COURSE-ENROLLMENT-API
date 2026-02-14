
from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

# -------------------------
# CREATE USERS
# -------------------------

def test_create_student():
    res = client.post(
        "/api/v1/users/",
        json={"name": "Student One", "email": "student1@test.com", "role": "student"}
    )
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Student One"
    assert data["email"] == "student1@test.com"
    assert data["role"] == "student"
    assert "id" in data


def test_create_admin():
    res = client.post(
        "/api/v1/users/",
        json={"name": "Admin User", "email": "admin@test.com", "role": "admin"}
    )
    assert res.status_code == 201
    data = res.json()
    assert data["role"] == "admin"


def test_create_user_invalid_data():
    # Missing name
    res = client.post("/api/v1/users/", json={"email": "bad@test.com", "role": "student"})
    assert res.status_code == 422

    # Missing email
    res = client.post("/api/v1/users/", json={"name": "NoEmail", "role": "student"})
    assert res.status_code == 422

    # Invalid role
    res = client.post("/api/v1/users/", json={"name": "InvalidRole", "email": "role@test.com", "role": "manager"})
    assert res.status_code == 422


def test_create_user_duplicate_email():
    # Create initial user
    client.post("/api/v1/users/", json={"name": "DupUser", "email": "dup@test.com", "role": "student"})
    
    # Try creating user with same email
    res = client.post("/api/v1/users/", json={"name": "DupUser2", "email": "dup@test.com", "role": "student"})
    assert res.status_code == 400
    assert "email" in res.json()["detail"].lower()


# -------------------------
# GET USERS
# -------------------------

def test_get_all_users():
    res = client.get("/api/v1/users/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert all("id" in user and "name" in user for user in data)


def test_get_user_by_id():
    # First create a user
    create_res = client.post("/api/v1/users/", json={"name": "SingleUser", "email": "single@test.com", "role": "student"})
    user_id = create_res.json()["id"]

    res = client.get(f"/api/v1/users/{user_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == user_id
    assert data["name"] == "SingleUser"


def test_get_user_not_found():
    res = client.get("/api/v1/users/9999")  # ID that doesn't exist
    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()
