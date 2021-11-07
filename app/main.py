from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm.session import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="social_media_platform",
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error", error)
        time.sleep(2)

my_posts = [
    {"title": "title1", "content": "content of post 1", "id": 1},
    {"title": "title2", "content": "content of post 2", "id": 2},
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts")
async def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {"data": "success"}
