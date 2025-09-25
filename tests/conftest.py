import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

from app.main import app
from app.dependencies import get_session
from app.schemas import UserInDb


TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


#fixture creating SQL Base
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)


#fixture creating FastAPI client
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()

#fixture creating sample film
@pytest.fixture
def sample_film(client):
    response = client.post("/films/", json = {
        "title" : "Film A", "director" : "Director A", "year" : 2000
    })
    return response.json()

@pytest.fixture
def sample_list_of_films(client):
    films = []
    for data in [
        {"id": i, "title": f"Film {chr(64+i)}", "year": 2000 + i, "director": f"Director {chr(64+i)}"}
        for i in range(1, 21)
    ]:
        response = client.post("/films/", json=data)
        films.append(response.json())

    return films

@pytest.fixture
def sample_list_of_reviews(client, sample_film, sample_user_registration, sample_user_login):
    film_id = sample_film['id']
    review_text = "Review test content"
    reviews = []
    
    for data in [
        {"film_id": film_id, "review_text": review_text, "rating": 2.3},
        {"film_id": film_id, "review_text": review_text, "rating": 5},
        {"film_id": film_id, "review_text": review_text, "rating": 4.33},
    ]:

        response = client.post(f"/films/{film_id}/reviews/", json = data,
                               headers= {
            "Authorization" : f"Bearer {sample_user_login['access_token']}"
        })
        reviews.append(response.json())
    
    return reviews

@pytest.fixture
def sample_user_registration(session):
    from app.models import User
    from app.security import hash_password

    hashed = hash_password("test_password")
    user = User(username="test_user", hashed_password=hashed, email="test@email.com")
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserInDb.model_validate(user)

@pytest.fixture
def sample_user_login(client, sample_user_registration):
    password = "test_password"
    
    response = client.post(
    "/auth/login",
    data={
        "username": sample_user_registration.username,
        "password": password},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return response.json()
    