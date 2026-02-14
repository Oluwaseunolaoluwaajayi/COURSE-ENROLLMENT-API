# Course Enrollment Management API

A **RESTful API** built with **FastAPI** to manage course enrollments for students and admins.

---

## Features

- Create and view users (students & admins)
- Publicly view courses
- Admins can create, update, and delete courses
- Students can enroll in and deregister from courses
- Admins can view all enrollments and force-deregister students
- Role-based access control via `X-User-Role` header
- In-memory data storage (no database required)
- Fully tested with **pytest**

---

## Tech Stack

- Python 3.10+
- FastAPI
- Pydantic
- Uvicorn
- pytest + httpx

---

## Project Structure

course-enrollment-api/
├── app/
│ ├── init.py
│ ├── main.py
│ ├── models.py
│ ├── schemas.py
│ ├── storage.py
│ ├── dependencies.py
│ └── routers/
│ ├── init.py
│ ├── users.py
│ ├── courses.py
│ └── enrollments.py
├── tests/
│ ├── init.py
│ ├── conftest.py
│ ├── test_users.py
│ ├── test_courses.py
│ └── test_enrollments.py
├── requirements.txt
└── README.md

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Oluwaseunolaoluwaajayi/COURSE-ENROLLMENT-API.git
cd course-enrollment-api

2. Create and activate a virtual environment

Windows (PowerShell):

python -m venv env
.\env\Scripts\Activate.ps1

Linux / MacOS:

python3 -m venv env
source env/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Run the API
uvicorn app.main:app --reload

Base URL: http://127.0.0.1:8000

Swagger UI: http://127.0.0.1:8000/api/v1/docs

ReDoc: http://127.0.0.1:8000/api/v1/redoc

OpenAPI JSON: http://127.0.0.1:8000/api/v1/openapi.json

All endpoints are versioned under /api/v1.


User Identification

No authentication is implemented.
Users are identified by passing the role header in requests:

X-User-Role: student
X-User-Role: admin


Running Tests

All tests are located in the tests/ directory.

Run the full test suite:

pytest


```
