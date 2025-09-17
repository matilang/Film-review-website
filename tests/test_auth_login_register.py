## registration and login tests
from app.crud import get_user
from app.auth import verify_password


def test_add_user(client):
    username = "test_user"
    password = "test_pass"
    email = "test_email"
    full_name = "test_full_name"
    response = client.post("/auth/register",
                           json={"username" : username, "password" : password, "email" : email, "full_name" : full_name})
    
    assert response.status_code == 201
    assert response.json()['username'] == username
    assert response.json()['email'] == email
    assert response.json()['full_name'] == full_name
    assert isinstance(response.json()['id'], int)
    assert response.json()['disabled'] == None

def test_check_duplicate_username(client, sample_user_registration):
    response = client.post("/auth/register",
                           json={"username" : sample_user_registration.username, "password" : "new_pass"})
    assert response.status_code == 409
    
def test_check_password(session, sample_user_registration):
    unhashed_password = "test_password"
    hashed_password = get_user(session, sample_user_registration.username).hashed_password
    assert verify_password(unhashed_password, hashed_password)

def test_login(client, sample_user_registration):
    password = "test_password"
    response = client.post(
        "/auth/login",
        data={
            "username": sample_user_registration.username,
            "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200

def test_wrong_login(client, sample_user_registration):
    password = "test_password"
    response = client.post(
        "/auth/login",
        data={
            "username": "wrong_username",
            "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    response = client.post(
        "/auth/login",
        data={
            "username": sample_user_registration.username,
            "password": "wrong_password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    