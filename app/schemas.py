from sqlmodel import Field
from pydantic import BaseModel

class FilmCreate(BaseModel):
    title : str
    director : str
    year : int = Field(gt=0)
    
class FilmRead(BaseModel):
    id : int
    title : str
    director : str
    year : int

class FilmUpdate(BaseModel):
    title : str | None = None
    director : str | None = None
    year : int | None = Field(default=None, ge=0)

class ReviewCreate(BaseModel):
    film_id : int
    review_text : str
    rating : float = Field(ge=1, le=5)

class ReviewRead(BaseModel):
    id : int
    film_id : int
    review_text : str
    rating : float
    
    model_config = {
       "from_attributes" : True
    }

class ReviewUpdate(BaseModel):
    review_text : str | None = None
    rating : float | None = Field(default=None, ge=1, le=5)
    
class UserCreate(BaseModel):
    username : str
    password : str
    email : str | None = None
    full_name : str | None = None
    
class UserRead(BaseModel):
    id : int
    username : str
    email : str | None
    full_name : str | None = None
    disabled : bool | None = None
    
    model_config = {
       "from_attributes" : True
    }

class UserInDb(UserRead):
    hashed_password : str
    
    model_config = {
       "from_attributes" : True
    }

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username : str | None = None