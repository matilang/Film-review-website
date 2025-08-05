from fastapi import APIRouter, Query, HTTPException, status
from ..dependencies import SessionDep
from ..models import Book
from ..schemas import BookUpdate, BookCreate, BookRead
from app import crud
from typing import Annotated
from sqlmodel import select


router = APIRouter(
    prefix="/books",
    tags=['books'],
    responses={404: {"description" : "Not found"}},
)

@router.get("/", response_model=list[BookRead])
async def get_list_of_books(session : SessionDep,
                            author: str | None = None,
                            year : int | None = None,
                            limit : Annotated[int | None, Query(gt=0, le=100)] = None,
                            offset : Annotated[int, Query(ge=0, le=100)] = 0,
                            ):
    books = crud.get_list_of_books(session, author, year, limit, offset)
    if not books:
        raise HTTPException(
            status_code=404,
            detail="No books found with this limits"
        )
    return books

@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(new_book : BookCreate, session : SessionDep):
    book = crud.create_book(new_book, session)
    if not book:
        raise HTTPException(status_code=404, detail="Couldn't create book")
    return book

@router.get("/{book_id}", response_model=BookRead)
async def get_book_by_id(book_id : int, session : SessionDep):
    book = crud.get_book_by_id(book_id, session)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.patch("/{book_id}", response_model=BookRead)
async def update_book(book_id : int, new_details : BookUpdate, session: SessionDep):
    book = crud.update_book(book_id, new_details, session)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}")
async def delete_book(book_id : int, session : SessionDep):
    succes = crud.delete_book(book_id, session)
    if not succes:
        raise HTTPException(status_code=404, detail="Book not found")

