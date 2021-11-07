from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users")


# CREATE USER
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# GET USER
@router.get("/{id}", response_model=schemas.User)
async def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.Post).filter(models.Post.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return user
