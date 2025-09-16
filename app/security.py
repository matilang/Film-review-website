import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from typing import Annotated

SECRET_KEY = "4363eb74075a5ac4486f15d36aef9fe507fe07d6c6b68e8cd69e196f991a78c6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

oauth2scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(plain_password : str):
    return pwd_context.hash(plain_password)

def verify_password(plain_password : str, hashed_password : str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data : dict, expires_delta : timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token : str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        return None