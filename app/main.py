from fastapi import FastAPI
from sqlmodel import SQLModel
from .routes import books, reviews
from .db import engine


SQLModel.metadata.create_all(engine)

app = FastAPI()

app.include_router(books.router)
app.include_router(reviews.router)

