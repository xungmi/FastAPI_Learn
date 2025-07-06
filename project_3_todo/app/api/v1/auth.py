# Chứa logic authentication và authorization


from fastapi import APIRouter, HTTPException, Depends, status
from ...models import Users
from passlib.context import CryptContext
from ...core.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ...core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DELTA
from datetime import datetime, timedelta, timezone
from jose import jwt
from ...schemas import CreateUserRequest, Token


# Khởi tạo đối tượng Bcrypt hashing để mã hóa mật khẩu
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Tạo router chung cho các endpoint liên quan đến authentication trong cùng 1 mục trong Swagger UI
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role : str, expires_delta: timedelta):
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": username,
        "id": user_id,
        "role": role,
        "exp": expire
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get("/users", status_code=status.HTTP_200_OK)
def read_all_users(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return {"users": users}


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(create_user_request: CreateUserRequest, db: Session = Depends(get_db)):
    user_data = create_user_request.dict()
    user_data["hashed_password"] = bcrypt_context.hash(user_data.pop("password"))
    user_data["is_active"] = True

    new_user = Users(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created", "user": new_user}


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(
        username=user.username,
        user_id=user.id,
        expires_delta=timedelta(minutes=3)
    )

    # Bearer : Server sẽ không kiểm tra danh tính người gửi, mà chỉ xác minh token có hợp lệ không.
    return {"access_token": token, "token_type": "bearer"}