from fastapi import APIRouter, HTTPException, Header
from app.schemas import CourseCreate, Course
from app.storage import courses, course_id_seq

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=Course, status_code=201)
def create_course(
    course: CourseCreate,
    x_user_role: str = Header(...)
):
    global course_id_seq

    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    
    for c in courses.values():
        if c["code"] == course.code:
            raise HTTPException(status_code=400, detail="Course code already exists")

    cid = course_id_seq
    courses[cid] = {
        "id": cid,
        "title": course.title,
        "code": course.code
    }
    course_id_seq += 1

    return courses[cid]


@router.get("/", response_model=list[Course])
def get_courses():
    return list(courses.values())


@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]
