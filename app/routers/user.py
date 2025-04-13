from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db

router = APIRouter(tags=["Users"])


# Creating a new user
@router.get(
    "/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut
)
def get_current_user(
    db: Session = Depends(get_db),
    user_data: schemas.User = Depends(oauth2.get_current_user),
):

    return schemas.UserOut(user=user_data)


# Getting a user by ID
@router.get("/users/{id}", response_model=schemas.UserOut)
def create_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    if not user_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with id: {id}",
        )
    user = user_query.first()
    return schemas.UserOut(user=schemas.User.model_validate(user))
