## authentication token tests
import jwt
from app.security import ALGORITHM, SECRET_KEY
from app.dependencies import get_current_user, get_current_active_user
from app.schemas import UserRead

def test_check_token(client, sample_user_registration):
    password = "test_password"
    response = client.post(
    "/auth/login",
    data={
        "username": sample_user_registration.username,
        "password": password},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    payload = jwt.decode(response.json()['access_token'], SECRET_KEY, algorithms=[ALGORITHM])
    assert payload['sub'] == sample_user_registration.username

def test_get_current_user(session, sample_user_registration, sample_user_login):
    user = get_current_user(sample_user_login['access_token'], session)
    assert isinstance(user, UserRead)