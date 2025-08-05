from ..schemas import ReviewCreate, ReviewUpdate, ReviewRead
from ..dependencies import SessionDep
from ..models import Book
from app import crud
from fastapi import APIRouter, Query, HTTPException


router = APIRouter(prefix="/books/{book_id}",
                   tags=["reviews"])

@router.post("/reviews", response_model=ReviewRead)
async def add_review(review : ReviewCreate, session : SessionDep):
    create_review = crud.add_review(review, session)
    if not create_review:
        raise HTTPException(status_code=404, detail="Book not found")
    return create_review

@router.get("/reviews", response_model=list[ReviewRead])
async def get_all_reviews(book_id : int, session: SessionDep):
    reviews_list = crud.get_all_reviews(book_id, session)
    if not reviews_list:
        raise HTTPException(status_code=404, detail="Reviews not found")
    return reviews_list
    
@router.get("/rating")
async def get_rating_average(book_id : int, session : SessionDep):
    rating = crud.get_rating_average(book_id, session)
    if not rating:
        raise HTTPException(status_code=404, detail="Reviews not found")
    return rating