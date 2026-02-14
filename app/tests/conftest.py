import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# -------------------------
# Fixture: create users & course
# -------------------------
@pytest.fixture
def setup_users_and_course():
    """Creates a student, an admin, and a course for testing."""

    # Helper functions
    def create_student(name="Student One", email="student1@test.com"):
        res = client.post(
            "/api/v1/users/",
            json={"name": name, "email": email, "role": "student"}
        )
        assert res.status_code == 201
        return res.json()["id"]

    def create_admin(name="Admin User", email="admin@test.com"):
        res = client.post(
            "/api/v1/users/",
            json={"name": name, "email": email, "role": "admin"}
        )
        assert res.status_code == 201
        return res.json()["id"]

    def create_course(admin_id, title="Math 101", code="MATH101"):
        res = client.post(
            "/api/v1/courses/",
            json={"title": title, "code": code},
            headers={"X-User-Role": "admin"}  # role in header
        )
        assert res.status_code == 201
        return res.json()["id"]

    student_id = create_student()
    admin_id = create_admin()
    course_id = create_course(admin_id)

    return {"student_id": student_id, "admin_id": admin_id, "course_id": course_id}
