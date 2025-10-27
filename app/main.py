from fastapi import FastAPI
from sqlmodel import SQLModel
from .routes import films, reviews
from .db import engine
from .auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

SQLModel.metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(films.router)
app.include_router(reviews.router)
app.include_router(auth_router)

