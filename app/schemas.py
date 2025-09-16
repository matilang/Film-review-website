from sqlmodel import Field
from pydantic import BaseModel

class BookCreate(BaseModel):
    title : str
    author : str
    year : int = Field(gt=0)
    
class BookRead(BaseModel):
    id : int
    title : str
    author : str
    year : int

class BookUpdate(BaseModel):
    title : str | None = None
    author : str | None = None
    year : int | None = Field(default=None, ge=0)

class ReviewCreate(BaseModel):
    book_id : int
    review_text : str
    rating : float = Field(ge=1, le=5)

class ReviewRead(BaseModel):
    id : int
    book_id : int
    review_text : str
    rating : float

class ReviewUpdate(BaseModel):
    review_text : str | None = None
    rating : float | None = Field(default=None, ge=1, le=5)
    
class UserCreate(BaseModel):
    id : int
    username : str
    password : str
    email : str | None
    full_name : str | None = None

class UserLogin(BaseModel):
    username : str
    password : str
    
class UserRead(BaseModel):
    id : int
    username : str
    email : str | None
    full_name : str | None = None
    disabled : bool | None = None

class UserInDb(UserRead):
    hashed_password : str
    
class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username : str | None = None