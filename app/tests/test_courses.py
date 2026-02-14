
from fastapi.testclient import TestClient
from app.main import app

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

# -------------------------
# CREATE COURSES
# -------------------------

def test_admin_can_create_course():
    admin_id = create_admin()
    res = client.post(
        "/api/v1/courses/",
        json={"title": "Physics 101", "code": "PHYS101"},
        headers={"X-User-Role": "admin"}
    )
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Physics 101"
    assert data["code"] == "PHYS101"
    assert "id" in data

def test_non_admin_cannot_create_course():
    student_id = create_student()
    res = client.post(
        "/api/v1/courses/",
        json={"title": "Chemistry 101", "code": "CHEM101"},
        headers={"X-User-Role": "student"}
    )
    assert res.status_code == 403

def test_duplicate_course_code_rejected():
    admin_id = create_admin(name="Admin2", email="admin2@test.com")
    # First creation
    client.post(
        "/api/v1/courses/",
        json={"title": "Math 101", "code": "MATH101"},
        headers={"X-User-Role": "admin"}
    )
    # Duplicate creation
    res = client.post(
        "/api/v1/courses/",
        json={"title": "Advanced Math", "code": "MATH101"},
        headers={"X-User-Role": "admin"}
    )
    assert res.status_code == 400
    assert "unique" in res.json()["detail"].lower()

# -------------------------
# GET COURSES
# -------------------------

def test_get_all_courses():
    res = client.get("/api/v1/courses/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)

def test_get_course_by_id():
    admin_id = create_admin(name="Admin3", email="admin3@test.com")
    create_res = client.post(
        "/api/v1/courses/",
        json={"title": "Biology 101", "code": "BIO101"},
        headers={"X-User-Role": "admin"}
    )
    course_id = create_res.json()["id"]

    res = client.get(f"/api/v1/courses/{course_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == course_id
    assert data["title"] == "Biology 101"

def test_get_course_not_found():
    res = client.get("/api/v1/courses/9999")
    assert res.status_code == 404

# -------------------------
# UPDATE COURSES
# -------------------------

def test_admin_can_update_course():
    admin_id = create_admin(name="Admin4", email="admin4@test.com")
    create_res = client.post(
        "/api/v1/courses/",
        json={"title": "History 101", "code": "HIST101"},
        headers={"X-User-Role": "admin"}
    )
    course_id = create_res.json()["id"]

    res = client.patch(
        f"/api/v1/courses/{course_id}",
        json={"title": "History 102", "code": "HIST102"},
        headers={"X-User-Role": "admin"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "History 102"
    assert data["code"] == "HIST102"

def test_non_admin_cannot_update_course():
    student_id = create_student(name="Student2", email="student2@test.com")
    # Admin creates course
    admin_id = create_admin(name="Admin5", email="admin5@test.com")
    create_res = client.post(
        "/api/v1/courses/",
        json={"title": "Geo 101", "code": "GEO101"},
        headers={"X-User-Role": "admin"}
    )
    course_id = create_res.json()["id"]

    res = client.patch(
        f"/api/v1/courses/{course_id}",
        json={"title": "Geo 102", "code": "GEO102"},
        headers={"X-User-Role": "student"}
    )
    assert res.status_code == 403

def test_update_course_duplicate_code():
    admin_id = create_admin(name="Admin6", email="admin6@test.com")
    # Create two courses
    c1 = client.post(
        "/api/v1/courses/",
        json={"title": "Course1", "code": "C1"},
        headers={"X-User-Role": "admin"}
    ).json()["id"]
    c2 = client.post(
        "/api/v1/courses/",
        json={"title": "Course2", "code": "C2"},
        headers={"X-User-Role": "admin"}
    ).json()["id"]

    # Attempt to update course2 to code C1
    res = client.patch(
        f"/api/v1/courses/{c2}",
        json={"title": "Course2 Updated", "code": "C1"},
        headers={"X-User-Role": "admin"}
    )
    assert res.status_code == 400

# -------------------------
# DELETE COURSES
# -------------------------

def test_admin_can_delete_course():
    admin_id = create_admin(name="Admin7", email="admin7@test.com")
    create_res = client.post(
        "/api/v1/courses/",
        json={"title": "Delete Me", "code": "DEL101"},
        headers={"X-User-Role": "admin"}
    )
    course_id = create_res.json()["id"]

    res = client.delete(
        f"/api/v1/courses/{course_id}",
        headers={"X-User-Role": "admin"}
    )
    assert res.status_code == 200
    assert "deleted" in res.json()["detail"].lower()

def test_non_admin_cannot_delete_course():
    student_id = create_student(name="Student3", email="student3@test.com")
    admin_id = create_admin(name="Admin8", email="admin8@test.com")
    create_res = client.post(
        "/api/v1/courses/",
        json={"title": "Cannot Delete", "code": "NODEL101"},
        headers={"X-User-Role": "admin"}
    )
    course_id = create_res.json()["id"]

    res = client.delete(
        f"/api/v1/courses/{course_id}",
        headers={"X-User-Role": "student"}
    )
    assert res.status_code == 403

def test_delete_course_not_found():
    admin_id = create_admin(name="Admin9", email="admin9@test.com")
    res = client.delete(
        "/api/v1/courses/9999",
        headers={"X-User-Role": "admin"}
    )
    assert res.status_code == 404
