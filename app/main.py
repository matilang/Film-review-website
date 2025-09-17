from fastapi import FastAPI
from sqlmodel import SQLModel
from .routes import books, reviews
from .db import engine
from .auth import router as auth_router

SQLModel.metadata.create_all(engine)

app = FastAPI()

app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(auth_router)

