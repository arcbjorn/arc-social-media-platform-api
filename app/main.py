from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import post_router, user_router, auth_router, vote_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(vote_router.router)
