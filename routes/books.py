from fastapi import APIRouter, Query, HTTPException, status
from ..dependencies import SessionDep
from ..models import Book, Review
from typing import Annotated
from sqlmodel import select

router = APIRouter(
    prefix="/books",
    tags=['books'],
    responses={404: {"description" : "Not found"}},
)

@router.get("/", response_model=list[Book])
async def get_list_of_books(session : SessionDep,
                            author: str | None = None,
                            year : int | None = None,
                            limit : Annotated[int | None, Query(gt=0, le=100)] = None,
                            offset : Annotated[int, Query(ge=0, le=100)] = 0,
                            ):
    statement = select(Book)
    
    if author:
        statement = statement.where(Book.author == author)
    if year:
        statement = statement.where(Book.year == year)

    books = session.exec(statement.offset(offset).limit(limit)).all()
    return books

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book : Book, session : SessionDep):
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@router.get("/{book_id}", response_model=Book)
async def get_book_by_id(book_id : int, session : SessionDep):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )
    return book
    