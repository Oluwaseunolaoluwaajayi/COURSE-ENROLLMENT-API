from pydantic import BaseModel, EmailStr, Field
from typing import Literal

# ---------------- USERS ----------------

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    role: Literal["student", "admin"]

class User(UserCreate):
    id: int


# ---------------- COURSES ----------------

class CourseCreate(BaseModel):
    title: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)

class Course(CourseCreate):
    id: int


# ---------------- ENROLLMENTS ----------------

class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int

class Enrollment(EnrollmentCreate):
    id: int
