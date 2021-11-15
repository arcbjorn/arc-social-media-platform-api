from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pytest import pytest

from app import schemas, models
from app.main import app
from app.config import env
from app.database import Base, get_db
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{env.db_username}:{env.db_password}@{env.db_hostname}:{env.db_port}/{env.db_name}_test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def session():
    Base.metadata.create_all(bind=engine)
    Base.metadata.drop_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def user_fixture(client):
    user_data = schemas.UserCreateDto(
        {
            "email": "test@example.com",
            "password": "secret",
        }
    )
    res = client.post("/users/", json=user_data.dict())

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token_fixture(user_fixture):
    return create_access_token(data={"user_id": user_fixture["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def posts_fixture(user_fixture, session):
    posts_data = [
        {
            "title": "1st title",
            "content": "1st content",
            "owner_id": user_fixture["id"],
        },
        {
            "title": "2st title",
            "content": "2st content",
            "owner_id": user_fixture["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    posts = list(map(create_post_model, posts_data))

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
