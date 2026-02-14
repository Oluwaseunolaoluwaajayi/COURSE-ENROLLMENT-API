# Course Enrollment Management API

A simple **RESTful API** built with **FastAPI** to manage course enrollments.

## Features

- Create and view users (students & admins)
- Publicly view courses
- Admins can create, update, and delete courses
- Students can enroll and deregister themselves from courses
- Admins can view all enrollments and force-deregister students
- Role-based access control using `X-User-ID` header
- In-memory data storage (no database)
- Automated tests with pytest

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
│ ├── database.py
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
git clone <your-repo-url>
cd course-enrollment-api

2. Create and activate a virtual environment

Windows (PowerShell):
python -m venv env
.\env\Scripts\Activate.ps1

python -m venv env
.\env\Scripts\Activate.ps1

pip install -r requirements.txt

uvicorn app.main:app --reload
The API will be available at:

Base URL: http://127.0.0.1:8000

Swagger UI: http://127.0.0.1:8000/api/v1/docs

ReDoc: http://127.0.0.1:8000/api/v1/redoc

OpenAPI JSON: http://127.0.0.1:8000/api/v1/openapi.json

All endpoints are versioned under /api/v1.

Authentication / User Identification

No authentication (JWT or sessions) is used.

Instead, the API identifies users using a request header:

X-User-ID: 1

Running Tests

All tests are located in the tests/ directory.

Run the full test suite:

pytest

Notes

All data is stored in memory

Restarting the server resets all data

HTTP status codes follow REST conventions (201, 204, 403, etc.)
```
