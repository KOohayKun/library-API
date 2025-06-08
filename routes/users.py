from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel
from Library.models.user_model import UserCreate
from Library.datab.dbmodels import Reader
from Library.datab.database import get_db
from Library.utils.security import hash_password, create_access_token, verify_password

router = APIRouter(prefix="/users")
access_token_expire_minutes = 30

class Message(BaseModel):
    message: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=Message)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Reader).filter(Reader.email == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь уже существует")
    hashed_pwd = hash_password(user.password)
    new_user = Reader(
        name=user.username,
        email=user.username,
        hashed_password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Пользователь зарегистрирован"}


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(Reader).filter(Reader.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль"
        )
    access_token_expires = timedelta(minutes=access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}