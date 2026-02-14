from fastapi import FastAPI
from app.routers import users, courses, enrollments
from pydantic import BaseModel

# API VERSION PREFIX
API_PREFIX = "/api/v1"

app = FastAPI(
    title="Course Enrollment Management API",
    version="1.0.0",
    docs_url=f"{API_PREFIX}/docs",      # optional: versioned docs
    openapi_url=f"{API_PREFIX}/openapi.json",
)

# I then APPLY VERSIONING HERE
app.include_router(users.router, prefix=API_PREFIX)
app.include_router(courses.router, prefix=API_PREFIX)
app.include_router(enrollments.router, prefix=API_PREFIX)


@app.get("/")
def root():
    return {
        "message": "Course Enrollment API is running",
        "docs": f"{API_PREFIX}/docs"
    }
