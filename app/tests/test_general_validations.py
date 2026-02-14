from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# -------------------------
# ROLE-BASED ACCESS
# -------------------------

def test_admin_only_action_forbidden_for_student():
    # Student tries to create a course
    res = client.post(
        "/api/v1/courses/",
        json={"title": "Forbidden Course", "code": "FORB101"},
        headers={"X-User-Role": "student"}
    )
    assert res.status_code == 403
    assert "forbidden" in res.json()["detail"].lower()


def test_student_only_action_forbidden_for_admin():
    # Admin tries to enroll
    res = client.post(
        "/api/v1/enrollments/",
        json={"user_id": 1, "course_id": 1},
        headers={"X-User-Role": "admin"}
    )
    assert res.status_code == 403
    assert "forbidden" in res.json()["detail"].lower()


# -------------------------
# REQUIRED FIELD VALIDATION
# -------------------------

def test_missing_required_fields_users():
    # Missing name
    res = client.post("/api/v1/users/", json={"email": "nofield@test.com", "role": "student"})
    assert res.status_code == 422

    # Missing email
    res = client.post("/api/v1/users/", json={"name": "NoEmail", "role": "student"})
    assert res.status_code == 422

def test_missing_required_fields_courses():
    # Missing title
    res = client.post("/api/v1/courses/", json={"code": "MISSING101"}, headers={"X-User-Role": "admin"})
    assert res.status_code == 422

    # Missing code
    res = client.post("/api/v1/courses/", json={"title": "NoCode"}, headers={"X-User-Role": "admin"})
    assert res.status_code == 422


# -------------------------
# DUPLICATE CHECK
# -------------------------

def test_duplicate_email_users():
    # Create initial user
    client.post("/api/v1/users/", json={"name": "DupUser", "email": "dup@test.com", "role": "student"})
    # Try creating with same email
    res = client.post("/api/v1/users/", json={"name": "DupUser2", "email": "dup@test.com", "role": "student"})
    assert res.status_code == 400
    assert "email" in res.json()["detail"].lower()

def test_duplicate_course_code():
    # Create initial course
    client.post("/api/v1/courses/", json={"title": "Course1", "code": "C1"}, headers={"X-User-Role": "admin"})
    # Try creating duplicate
    res = client.post("/api/v1/courses/", json={"title": "Course2", "code": "C1"}, headers={"X-User-Role": "admin"})
    assert res.status_code == 400
    assert "unique" in res.json()["detail"].lower()


# -------------------------
# STATUS CODES
# -------------------------

def test_create_returns_201():
    res = client.post("/api/v1/users/", json={"name": "StatusTest", "email": "status@test.com", "role": "student"})
    assert res.status_code == 201

def test_delete_returns_404_for_nonexistent():
    res = client.delete("/api/v1/courses/9999", headers={"X-User-Role": "admin"})
    assert res.status_code == 404

def test_forbidden_returns_403():
    res = client.post("/api/v1/courses/", json={"title": "Forbidden", "code": "FORB"}, headers={"X-User-Role": "student"})
    assert res.status_code == 403

def test_invalid_input_returns_422():
    res = client.post("/api/v1/users/", json={"name": 123, "email": "bad@test.com", "role": "student"})
    assert res.status_code == 422
