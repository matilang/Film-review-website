from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from datetime import timedelta
from .schemas import UserCreate, UserRead, Token
from .dependencies import SessionDep, Session
from .security import verify_password
from .models import User
from .crud import get_user, add_user
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

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def user_register(user : UserCreate, session : SessionDep):
    db_user = add_user(session, user)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong username or password")
    return UserRead.model_validate(db_user)

@router.post("/login", response_model=Token)
async def user_login(session : SessionDep, form_data : OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(session, form_data.username, form_data.password)
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
