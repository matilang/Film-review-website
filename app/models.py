from sqlmodel import SQLModel, Field, Relationship


class Film(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    title : str
    director : str
    year : int = Field(gt=0)
    
    review : list["Review"] = Relationship(back_populates="film")

class User(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    username : str
    hashed_password : str
    email : str | None = None
    full_name : str | None = None
    disabled : bool | None = None
    
    reviews : list["Review"] = Relationship(back_populates="user")
    
class Review(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    review_text : str
    rating : float = Field(ge=1, le=5)
    
    film_id : int = Field(foreign_key="film.id")
    film : Film = Relationship(back_populates="review")
    
    user_id : int = Field(foreign_key="user.id")
    user : User = Relationship(back_populates="reviews")
    
