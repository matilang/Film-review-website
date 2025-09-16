from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from datetime import timedelta
from .main import app
from .schemas import UserCreate, UserLogin, UserRead, UserInDb, Token
from .dependencies import SessionDep, Session
from .security import hash_password, verify_password
from .models import User
from .crud import get_user
from .security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

def authenticate_user(db : Session, username : str, password : str):
    user = get_user(db, username)
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

router = APIRouter(
    prefix="/auth",
    tags=['auth'],
)

@router.post("/register", response_model=UserRead)
async def user_register(user : UserCreate, session : SessionDep):
    hashed_password = hash_password(user.password)
    db_user = User(username = user.username, hashed_password=hashed_password, email=user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def user_login(user : UserLogin, session : SessionDep):
    user = authenticate_user(session, user.username, user.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub" : user.username}, expires_delta=access_token_expires
        )
    return Token(access_token=access_token, token_type="bearer")
