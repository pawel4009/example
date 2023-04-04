from app import schemas
import pytest
from jose import jwt
from app.config import settings


# def test_root(client):
#     res = client.get('/')
#     assert res.json().get('message') == 'Welcome to my API!!!!!!!!!!!'
#     assert res.status_code == 202


def test_user_create(client):
    res = client.post("/users/", json = {"email": "a@gmail.com", "password": "a123"}) # in the previous version we have to set /users/ because fastapi was redirecting every query to the /../ and throw 307 status code, so our test could fail
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "a@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data = {"username": test_user["email"], "password": test_user["password"]}) # login should be sent as a form data
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, settings.algorithm)
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrong_email", "a123", 403),
    ("a@gmail.com", "wrong_password", 403),
    ("wrong_email", "wrong_password", 403),
    ("a@gmail.com", None, 422),
    (None, "a123", 422),
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data = {"username": email, "password": password})
    assert res.status_code == status_code