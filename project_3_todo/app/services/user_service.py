from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models import Users
from app.schemas import UserVerification

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(user_id: int, db: Session):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def change_user_password(user_id: int, data: UserVerification, db: Session):
    user_model = db.query(Users).filter(Users.id == user_id).first()

    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt_context.verify(data.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change")

    user_model.hashed_password = bcrypt_context.hash(data.new_password)
    db.add(user_model)
    db.commit()
