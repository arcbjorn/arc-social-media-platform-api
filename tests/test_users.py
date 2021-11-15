from jose import jwt
import pytest
from app import schemas
from app.config import env


def test_create_user(client):
    new_user = schemas.UserCreateDto(
        {
            "email": "test@example.com",
            "password": "secret",
        }
    )

    res = client.post("/users/", json=new_user.dict())

    new_user = schemas.User(**res.json())
    assert new_user.email == "test@example.com"
    assert res.status_code == 201


def test_login_user(client, user_fixture):
    new_user = schemas.UserLoginDto(
        {
            "username": user_fixture["email"],
            "password": user_fixture["password"],
        }
    )

    res = client.post("/login", data=new_user.dict())

    login_res = schemas.Token(**res.json)

    payload = jwt.decode(
        login_res.access_token, env.secret_key, algorithms=[env.algorithm]
    )
    id: str = payload.get("user_id")

    assert id == user_fixture["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "secret", 403),
        ("test@example.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "secret", 422),
        ("test@example.com", None, 422),
    ],
)
def test_incorrect_login_user(client, user_fixture):
    new_user = schemas.UserLoginDto(
        {
            "username": user_fixture["email"],
            "password": "wrongpassword",
        }
    )

    res = client.post("/login", data=new_user.dict())

    assert res.status_code == 403
    # assert res.json().get("detail") == "Invalid Credentials"
