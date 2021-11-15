import pytest
from app import schemas


def test_get_all_post(authorized_client, posts_fixture):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.Post(**post)

    posts = list(map(validate, res.json()))

    assert res.status_code == 200
    assert len(res.json()) == len(posts_fixture)
    assert posts[0].Post.id == posts_fixture[0].id


def test_unauthorized_user_get_all_posts(client):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, posts_fixture):
    res = client.get(f"/posts/{posts_fixture[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(client, posts_fixture):
    res = client.get("/posts/111")
    assert res.status_code == 404


def test_get_one_post(authorized_client, posts_fixture):
    res = authorized_client.get(f"/posts/{posts_fixture[0].id}")

    assert res.status_code == 404

    post = schemas.Post(**res.json())
    assert post.Post.id == posts_fixture[0].id
    assert post.Post.title == posts_fixture[0].title
    assert post.Post.content == posts_fixture[0].content


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("title 1", "content 1", True),
        ("title 2", "content 2", False),
        ("title 3", "content 3", True),
    ],
)
def test_create_post(
    authorized_client, user_fixture, posts_fixture, title, content, published
):
    new_post = {"title": title, "content": content, "published": published}

    res = authorized_client.post("/posts/", json=new_post)
    created_post = schemas.Post(**res.json())

    assert res.status_code == 201

    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == user_fixture["id"]


def test_create_post_default_published_true(
    authorized_client, user_fixture, posts_fixture
):
    new_post = {"title": "title 1", "content": "content 1"}

    res = authorized_client.post("/posts/", json=new_post)
    created_post = schemas.Post(**res.json())

    assert res.status_code == 201

    assert created_post.title == "title 1"
    assert created_post.content == "content 1"
    assert created_post.published is True
    assert created_post.owner_id == user_fixture["id"]


def test_unauthorized_user_create_post(client, user_fixture, posts_fixture):
    new_post = {"title": "title 1", "content": "content 1"}
    res = client.post("/posts/", json=new_post)

    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, posts_fixture):
    res = client.delete(f"/posts/{posts_fixture[0].id}")

    assert res.status_code == 401


def test_delete_post(authorized_client, user_fixture, posts_fixture):
    res = authorized_client.delete(f"/posts/{posts_fixture[0].id}")

    assert res.status_code == 404


def test_delete_post_non_exist(authorized_client, user_fixture, posts_fixture):
    res = authorized_client.delete("/posts/111")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, user_fixture, posts_fixture):
    res = authorized_client.delete("/posts/111")

    assert res.status_code == 404


def test_update_post(authorized_client, user_fixture, posts_fixture):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": posts_fixture[0].id,
    }

    res = authorized_client.put(f"/posts/{posts_fixture[0].id}", json=data)
    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
