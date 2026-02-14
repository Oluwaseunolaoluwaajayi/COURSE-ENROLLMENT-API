from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate, User
from app.storage import users, user_id_seq
from email_validator import validate_email, EmailNotValidError

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate):
    global user_id_seq

    # duplicate email check
    for u in users.values():
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already exists")

    uid = user_id_seq
    users[uid] = {"id": uid, **user.dict()}
    user_id_seq += 1

    return users[uid]


@router.get("/", response_model=list[User])
def get_users():
    return list(users.values())

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]


