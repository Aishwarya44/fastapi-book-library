from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import Users
from database import SessionLocal
from sqlalchemy.sql.functions import current_user

router = APIRouter()

class User_schema(BaseModel):
    email: str
    password: str
    active: bool
    username: str
    firstName: str
    lastName: str

@router.get("/get_user")
def get_user():
    db: SessionLocal = SessionLocal()
    all_users = db.query(Users).all()
    return all_users

@router.post("/create_user")
def create_user(user: User_schema):
    db: SessionLocal = SessionLocal()

    existing_user = db.query(Users).filter(Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = Users(
        email=user.email,
        username=user.username,
        first_name=user.firstName,
        last_name=user.lastName,
        active=user.active,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/update_user/{id}")
def update_user(user: User_schema, id: int):
    db: SessionLocal = SessionLocal()
    existing_user = db.query(Users).filter(Users.id == id).first()
    print(existing_user)
    if existing_user:
        existing_user.email = user.email
        existing_user.first_name = user.firstName
        existing_user.last_name = user.lastName
        existing_user.active = user.active
        existing_user.password = user.password
        existing_user.username = user.username

        db.commit()
        db.refresh(existing_user)
        return existing_user
    else:
        raise HTTPException(status_code=400, detail="User not registered")

@router.delete("/delete_user/{id}")
def delete_user(id: int):
    db: SessionLocal = SessionLocal()
    existing_user = db.query(Users).filter(Users.id == id).first()
    if existing_user:
        db.delete(existing_user)
        db.commit()
        return "User deleted"
    else:
        raise HTTPException(status_code=400, detail="User not registered")








