from ..schemas import ReviewCreate, ReviewRead
from ..dependencies import SessionDep, UserDep
from app import crud
from fastapi import APIRouter, HTTPException, status


router = APIRouter(prefix="/films/{film_id}",
                   tags=["reviews"])

@router.post("/reviews", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def add_review(review : ReviewCreate,
                     session : SessionDep,
                     current_user : UserDep
                     ):
    create_review = crud.add_review(review, session, current_user)
    if not create_review:
        raise HTTPException(status_code=404, detail="Film not found")
    # backgroundemail.add_task(write_message,"my.email@wp.pl", "Review created!!")
    return create_review

@router.get("/reviews", response_model=list[ReviewRead])
async def get_all_reviews(film_id : int, session: SessionDep):
    reviews_list = crud.get_all_reviews(film_id, session)
    if not reviews_list:
        raise HTTPException(status_code=404, detail="Reviews not found")
    return reviews_list
    
@router.get("/rating")
async def get_rating_average(film_id : int, session : SessionDep):
    rating = crud.get_rating_average(film_id, session)
    if not rating:
        raise HTTPException(status_code=404, detail="Reviews not found")
    return rating