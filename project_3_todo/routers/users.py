from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import Annotated
from database import get_db
from .auth import get_current_user
from core.config import SECRET_KEY, ALGORITHM
from schemas import UserVerification
import models
from passlib.context import CryptContext

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


DBDependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/", status_code=200)
async def get_user(user: user_dependency, db: DBDependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    return db.query(models.Users).filter(models.Users.id == user["id"]).first()


@router.put("/password", status_code=204)
async def change_password(
    user: user_dependency,
    db: DBDependency,
    user_verification: UserVerification
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    user_model = db.query(models.Users).filter(models.Users.id == user["id"]).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model) # cập nhật lại user_model vào user đã có trong database
    db.commit()