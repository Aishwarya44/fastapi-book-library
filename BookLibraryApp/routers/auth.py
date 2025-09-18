from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from models import Users
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from jose import jwt, JWTError
from starlette import status
from sqlalchemy.orm import Session

router = APIRouter()

SECRET_KEY = '87328743573465743'
ALGORITHM = 'HS256'

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class User_schema(BaseModel):
    email: str
    password: str
    active: bool
    username: str
    firstName: str
    lastName: str

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(username: str, password: str, db: db_dependency):
    existing_user = db.query(Users).filter(Users.username == username).first()
    if not existing_user:
        return False
    if not password == existing_user.password:
        return False
    return existing_user

def create_access_token(username:str, user_id:int,  expires_delta:timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload", payload)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    authenticated_user = authenticate_user(form_data.username, form_data.password, db)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="User Authentication Failed")
    token = create_access_token(authenticated_user.username, authenticated_user.id, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}

@router.get("/get-users")
def get_users(db: db_dependency):
    all_users = db.query(Users).all()
    return all_users

@router.post("/create-user")
def create_user(user: User_schema, db: db_dependency):
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

@router.put("/update-user/{id}")
def update_user(user: User_schema, id: int, db: db_dependency):
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

@router.delete("/delete-user/{id}")
def delete_user(id: int, db: db_dependency):
    existing_user = db.query(Users).filter(Users.id == id).first()
    if existing_user:
        db.delete(existing_user)
        db.commit()
        return "User deleted"
    else:
        raise HTTPException(status_code=400, detail="User not registered")



