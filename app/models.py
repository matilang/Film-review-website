from sqlmodel import SQLModel, Field, Relationship


class Film(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    title : str
    director : str
    year : int = Field(gt=0)
    review : list["Review"] = Relationship(back_populates="film")

class Review(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    film_id : int = Field(foreign_key="film.id")
    review_text : str
    rating : float = Field(ge=1, le=5)
    
    film : Film = Relationship(back_populates="review")

class User(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    username : str
    hashed_password : str
    email : str | None = None
    full_name : str | None = None
    disabled : bool | None = None