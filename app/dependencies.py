from fastapi import Depends, status, HTTPException
from .db import engine
from typing import Annotated
from sqlmodel import Session
from .security import oauth2scheme, decode_access_token
from jwt.exceptions import InvalidTokenError
from .crud import get_user
from .schemas import UserInDb, UserRead

def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]

def get_current_user(token : Annotated[str, Depends(oauth2scheme)], db : SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return UserRead.model_validate(user)

UserDep = Annotated[UserInDb, Depends(get_current_user)]

def get_current_active_user(current_user : Annotated[UserRead, Depends(get_current_user)]):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

