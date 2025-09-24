from fastapi import APIRouter, Query, HTTPException, status
from ..dependencies import SessionDep
from ..schemas import FilmUpdate, FilmCreate, FilmRead
from app import crud
from typing import Annotated


router = APIRouter(
    prefix="/films",
    tags=['films'],
    responses={404: {"description" : "Not found"}},
)

@router.get("/", response_model=list[FilmRead])
async def get_list_of_films(session : SessionDep,
                            offset : Annotated[int, Query(ge=0, le=100)] = 0,
                            director: str | None = None,
                            year : int | None = None,
                            limit : Annotated[int | None, Query(gt=0, le=100)] = None,
                            sort_by : Annotated[str | None, Query(enum = ["title", "year"])] = None,
                            ):
    print(f"FROM ENDPOINT: sort_by = {sort_by}, type = {type(sort_by)}")
    films = crud.get_list_of_films(session, offset, director, year, limit, sort_by)
    if not films:
        raise HTTPException(
            status_code=404,
            detail="No films found with this limits"
        )
    return films

@router.post("/", response_model=FilmRead, status_code=status.HTTP_201_CREATED)
async def create_film(new_film : FilmCreate, session : SessionDep):
    film = crud.create_film(new_film, session)
    if not film:
        raise HTTPException(status_code=404, detail="Couldn't create film")
    return film

@router.get("/{film_id}", response_model=FilmRead)
async def get_film_by_id(film_id : int, session : SessionDep):
    film = crud.get_film_by_id(film_id, session)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film

@router.patch("/{film_id}", response_model=FilmRead)
async def update_film(film_id : int, new_details : FilmUpdate, session: SessionDep):
    film = crud.update_film(film_id, new_details, session)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film

@router.delete("/{film_id}")
async def delete_film(film_id : int, session : SessionDep):
    succes = crud.delete_film(film_id, session)
    if not succes:
        raise HTTPException(status_code=404, detail="Film not found")

