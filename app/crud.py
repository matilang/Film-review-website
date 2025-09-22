from .models import Film, Review, User
from .schemas import FilmCreate, FilmUpdate, ReviewCreate, UserInDb, ReviewRead, UserCreate
from fastapi import HTTPException, status
from sqlmodel import select, func, Session
from .security import hash_password

def get_list_of_films(db : Session,
                            offset : int,
                            author: str | None = None,
                            year : int | None = None,
                            limit : int | None = None,
                            sort_by : str | None = None,
                            ):
    statement = select(Film)
    if author:
        statement = statement.where(Film.author == author)
    if year:
        statement = statement.where(Film.year == year)
    if limit:
        statement = statement.limit(limit)
    if sort_by:
        column = getattr(Film, sort_by)
        statement = statement.order_by(column)
    count_films = select(func.count()).select_from(statement.subquery())
    count_films = db.exec(count_films).one()
    if offset > count_films:
        raise HTTPException(status_code=404, detail=f"Offset {offset} exeeds total number of matching films {count_films}")
    films = db.exec(statement.offset(offset)).all()
    return films

def create_film(new_film : FilmCreate, db : Session):
    film = Film(**new_film.model_dump())
    db.add(film)
    db.commit()
    db.refresh(film)
    return film

def get_film_by_id(film_id : int, db : Session):
    film = db.get(Film, film_id)
    return film

def update_film(film_id : int, new_details : FilmUpdate, db: Session):
    film = db.get(Film, film_id)
    if new_details.author:
        film.author = new_details.author
    if new_details.title:
        film.title = new_details.title
    if new_details.year:
        film.year = new_details.year
    db.commit()
    db.refresh(film)
    return film

def delete_film(film_id : int, db : Session):
    film = db.get(Film, film_id)
    if not film:
        return False
    db.delete(film)
    db.commit()
    return True

def add_review(review : ReviewCreate, db : Session):
    film = db.get(Film, review.film_id)
    if not film:
        return None
    new_review = Review(**review.model_dump())
    new_review.film = film
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return ReviewRead.model_validate(new_review)

def get_all_reviews(film_id : int, db: Session):
    statement = select(Review).where(Review.film_id == film_id)
    result = db.exec(statement).all()
    return [ReviewRead.model_validate(r) for r in result]
        
def get_rating_average(film_id : int, db : Session):
    statement = select(func.avg(Review.rating)).where(Review.film_id == film_id)
    average = db.exec(statement).all()
    rating = average[0]
    return rating

def get_user(db : Session, username : str):
    result = db.exec(select(User).where(User.username == username)).first()
    if result:
        return UserInDb.model_validate(result)

def add_user(db : Session, user : UserCreate):
    hashed_password = hash_password(user.password)
    check_existing_user = db.exec(select(User).where(User.username == user.username)).first()
    if check_existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
    db_user = User(**user.model_dump(exclude={"password"}), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserInDb.model_validate(db_user)