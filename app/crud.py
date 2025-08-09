from .models import Book, Review
from .dependencies import SessionDep
from .schemas import BookCreate, BookRead, BookUpdate, ReviewCreate
from fastapi import HTTPException
from sqlmodel import select, func

def get_list_of_books(session : SessionDep,
                            offset : int,
                            author: str | None = None,
                            year : int | None = None,
                            limit : int | None = None,
                            sort_by : str | None = None,
                            ):
    statement = select(Book)
    if author:
        statement = statement.where(Book.author == author)
    if year:
        statement = statement.where(Book.year == year)
    if limit:
        statement = statement.limit(limit)
    if sort_by:
        column = getattr(Book, sort_by)
        statement = statement.order_by(column)
    count_books = select(func.count()).select_from(statement.subquery())
    count_books = session.exec(count_books).one()
    if offset > count_books:
        raise HTTPException(status_code=404, detail=f"Offset {offset} exeeds total number of matching books {count_books}")
    books = session.exec(statement.offset(offset)).all()
    return books

def create_book(new_book : BookCreate, session : SessionDep):
    book = Book(**new_book.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

def get_book_by_id(book_id : int, session : SessionDep):
    book = session.get(Book, book_id)
    return book

def update_book(book_id : int, new_details : BookUpdate, session: SessionDep):
    book = session.get(Book, book_id)
    if new_details.author:
        book.author = new_details.author
    if new_details.title:
        book.title = new_details.title
    if new_details.year:
        book.year = new_details.year
    session.commit()
    session.refresh(book)
    return book

def delete_book(book_id : int, session : SessionDep):
    book = session.get(Book, book_id)
    if not book:
        return False
    session.delete(book)
    session.commit()
    return True

def add_review(review : ReviewCreate, session : SessionDep):
    book = session.get(Book, review.book_id)
    if not book:
        return None
    new_review = Review(**review.model_dump())
    new_review.book = book
    session.add(new_review)
    session.commit()
    session.refresh(new_review)
    return new_review

def get_all_reviews(book_id : int, session: SessionDep):
    statement = select(Review).where(Review.book_id == book_id)
    result = session.exec(statement).all()
    return result
        
def get_rating_average(book_id : int, session : SessionDep):
    statement = select(func.avg(Review.rating)).where(Review.book_id == book_id)
    average = session.exec(statement).all()
    rating = average[0]
    return rating
        