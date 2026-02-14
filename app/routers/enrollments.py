from fastapi import APIRouter, HTTPException, Header
from app.schemas import EnrollmentCreate, Enrollment
from app.storage import enrollments, enrollment_id_seq, users, courses

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

# These endpoints allow students to enroll/deregister themselves and view their enrollments. Adims can view all enrollments and mange them as needed.

@router.post("/", response_model=Enrollment, status_code=201)
def enroll_student(enroll: EnrollmentCreate, x_user_role: str = Header(...)):
    global enrollment_id_seq

    if x_user_role != "student":
        raise HTTPException(status_code=403, detail="Students only")

    if enroll.user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    if enroll.course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")

    if any(
        e["user_id"] == enroll.user_id and e["course_id"] == enroll.course_id
        for e in enrollments.values()
    ):
        raise HTTPException(status_code=400, detail="Already enrolled")

    eid = enrollment_id_seq
    enrollments[eid] = {
        "id": eid,
        "user_id": enroll.user_id,
        "course_id": enroll.course_id,
    }
    enrollment_id_seq += 1
    return enrollments[eid]

@router.get("/")
def get_enrollments(
    x_user_role: str = Header(...),
    x_user_id: int | None = Header(None)
):
    if x_user_role == "admin":
        return list(enrollments.values())

    if x_user_role == "student":
        return [e for e in enrollments.values() if e["user_id"] == x_user_id]

    raise HTTPException(status_code=403, detail="Invalid role")

@router.delete("/{enrollment_id}")
def deregister(enrollment_id: int, x_user_role: str = Header(...)):
    if enrollment_id not in enrollments:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    if x_user_role not in ("student", "admin"):
        raise HTTPException(status_code=403, detail="Forbidden")

    del enrollments[enrollment_id]
    return {"detail": "Enrollment deregistered"}
