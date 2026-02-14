
from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

# -------------------------
# HELPERS
# -------------------------
def create_admin(name="Admin", email="admin@test.com"):
    res = client.post(
        "/api/v1/users/",
        json={"name": name, "email": email, "role": "admin"}
    )
    return res.json()["id"]

def create_student(name="Student", email="student@test.com"):
    res = client.post(
        "/api/v1/users/",
        json={"name": name, "email": email, "role": "student"}
    )
    return res.json()["id"]

def create_course(admin_id, title="Test Course", code="TEST101"):
    res = client.post(
        "/api/v1/courses/",
        json={"title": title, "code": code},
        headers={"X-User-Role": "admin"}
    )
    return res.json()["id"]

# -------------------------
# FIXTURE: create users & course
# -------------------------
@pytest.fixture
def setup_users_and_course():
    student_id = create_student()
    admin_id = create_admin(name="Admin2", email="admin2@test.com")
    course_id = create_course(admin_id)
    return {"student_id": student_id, "admin_id": admin_id, "course_id": course_id}

# -------------------------
# ENROLLMENT TESTS
# -------------------------

def test_student_can_enroll(setup_users_and_course):
    ids = setup_users_and_course
    student_id = ids["student_id"]
    course_id = ids["course_id"]

    res = client.post(
        "/api/v1/enrollments/",
        json={"user_id": student_id, "course_id": course_id},
        headers={"X-User-Role": "student"}
    )
    assert res.status_code == 201
    data = res.json()
    assert data["user_id"] == student_id
    assert data["course_id"] == course_id

def test_admin_cannot_enroll(setup_users_and_course):
    ids = setup_users_and_course
    admin_id = ids["admin_id"]
    course_id = ids["course_id"]

    res = client.post(
        "/api/v1/enrollments/",
        json={"user_id": admin_id, "course_id": course_id},
        headers={"X-User-Role": "admin"}
    )
    assert res.status_code == 403

def test_student_cannot_enroll_twice(setup_users_and_course):
    ids = setup_users_and_course
    student_id = ids["student_id"]
    course_id = ids["course_id"]

    # First enrollment
    client.post(
        "/api/v1/enrollments/",
        json={"user_id": student_id, "course_id": course_id},
        headers={"X-User-Role": "student"}
    )

    # Duplicate enrollment
    res = client.post(
        "/api/v1/enrollments/",
        json={"user_id": student_id, "course_id": course_id},
        headers={"X-User-Role": "student"}
    )
    assert res.status_code == 400
    assert "already enrolled" in res.json()["detail"].lower()

def test_student_can_deregister(setup_users_and_course):
    ids = setup_users_and_course
    student_id = ids["student_id"]
    course_id = ids["course_id"]

    # Enroll first
    enroll_res = client.post(
        "/api/v1/enrollments/",
        json={"user_id": student_id, "course_id": course_id},
        headers={"X-User-Role": "student"}
    )
    enroll_id = enroll_res.json()["id"]

    # Deregister
    res = client.delete(
        f"/api/v1/enrollments/{enroll_id}",
        headers={"X-User-Role": "student"}
    )
    assert res.status_code == 200
    assert "deregistered" in res.json()["detail"].lower()

def test_admin_can_force_deregister(setup_users_and_course):
    ids = setup_users_and_course
    student_id = ids["student_id"]
    course_id = ids["course_id"]
    admin_id = ids["admin_id"]

    enroll_res = client.post(
        "/api/v1/enrollments/",
        json={"user_id": student_id, "course_id": course_id},
        headers={"X-User-Role": "student"}
    )
    enroll_id = enroll_res.json()["id"]

    res = client.delete(
        f"/api/v1/enrollments/{enroll_id}",
        headers={"X-User-Role": "admin"}
    )
    assert res.status_code == 200

def test_student_views_own_enrollments(setup_users_and_course):
    ids = setup_users_and_course
    student_id = ids["student_id"]
    course_id = ids["course_id"]

    # Enroll student
    client.post(
        "/api/v1/enrollments/",
        json={"user_id": student_id, "course_id": course_id},
        headers={"X-User-Role": "student"}
    )

    # Get enrollments
    res = client.get(
        "/api/v1/enrollments/",
        headers={"X-User-Role": "student", "X-User-ID": str(student_id)}
    )
    assert res.status_code == 200
    data = res.json()
    assert all(e["user_id"] == student_id for e in data)

def test_enroll_non_existing_user_or_course():
    # Non-existent user
    res1 = client.post(
        "/api/v1/enrollments/",
        json={"user_id": 9999, "course_id": 1},
        headers={"X-User-Role": "student"}
    )
    assert res1.status_code == 404

    # Non-existent course
    student_id = create_student(name="EdgeCase", email="edge@test.com")
    res2 = client.post(
        "/api/v1/enrollments/",
        json={"user_id": student_id, "course_id": 9999},
        headers={"X-User-Role": "student"}
    )
    assert res2.status_code == 404
