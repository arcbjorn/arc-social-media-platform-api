from fastapi import FastAPI

from . import models
from .database import engine
from .routers import posts_router, user_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts_router.router)
app.include_router(user_router.router)
