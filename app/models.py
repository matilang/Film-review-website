from sqlmodel import SQLModel, Field, Relationship


class Book(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    title : str
    author : str
    year : int = Field(gt=0)
    review : list["Review"] = Relationship(back_populates="book")

class Review(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    book_id : int = Field(foreign_key="book.id")
    review_text : str
    rating : float = Field(ge=1, le=5)
    
    book : Book = Relationship(back_populates="review")