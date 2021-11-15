from sqlalchemy.orm import session
from app.models import Vote
import pytest


@pytest.fixture()
def vote_fixture(authorized_client, user_fixture, posts_fixture):
    new_vote = Vote(post_id=posts_fixture[3].id, user_id=user_fixture["id"])

    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, posts_fixture):
    res = authorized_client.post(
        "/vote/", json={"post_id": posts_fixture[3].id, "dir": 1}
    )

    assert res.status_code == 201


def test_vote_twice(authorized_client, posts_fixture, vote_fixture):
    new_vote = {"post_id": posts_fixture[3].id, "dir": 1}
    res = authorized_client.post("/vote/", json=new_vote)

    assert res.status_code == 409


def test_delete(authorized_client, posts_fixture, vote_fixture):
    new_vote = {"post_id": posts_fixture[3].id, "dir": 0}
    res = authorized_client.delete("/vote/", json=new_vote)

    assert res.status_code == 201


def test_delete_vote_non_exist(authorized_client, posts_fixture):
    new_vote = {"post_id": posts_fixture[3].id, "dir": 0}
    res = authorized_client.delete("/vote/", json=new_vote)

    assert res.status_code == 404


def test_vote_post_non_exist(authorized_client, posts_fixture):
    new_vote = {"post_id": 11111, "dir": 1}
    res = authorized_client.post("/vote/", json=new_vote)

    assert res.status_code == 404


def test_vote_unauthorized_user(client, posts_fixture):
    new_vote = {"post_id": 11111, "dir": 1}
    res = client.post("/vote/", json=new_vote)

    assert res.status_code == 401
