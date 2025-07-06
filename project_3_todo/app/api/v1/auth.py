# Chỉ chứa phần routing
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import CreateUserRequest, Token
from app.services.auth_service import (
    authenticate_user_and_get_token,
    get_all_users,
    register_user,
)

# Tạo router chung cho các endpoint liên quan đến authentication trong cùng 1 mục trong Swagger UI
router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/users", status_code=status.HTTP_200_OK)
def read_all_users(db: Session = Depends(get_db)):
    return {"users": get_all_users(db)}


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(create_user_request: CreateUserRequest, db: Session = Depends(get_db)):
    user = register_user(create_user_request, db)
    return {"message": "User created", "user": user}


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    return authenticate_user_and_get_token(form_data.username, form_data.password, db)
