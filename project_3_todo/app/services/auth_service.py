from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import ACCESS_TOKEN_EXPIRE_DELTA, ALGORITHM, SECRET_KEY
from app.models import Users
from app.schemas import CreateUserRequest

# Khởi tạo đối tượng Bcrypt hashing để mã hóa mật khẩu
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_all_users(db: Session):
    return db.query(Users).all()


def register_user(create_user_request: CreateUserRequest, db: Session):
    user_data = create_user_request.dict()
    user_data["hashed_password"] = bcrypt_context.hash(user_data.pop("password"))
    user_data["is_active"] = True

    new_user = Users(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user or not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": username, "id": user_id, "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user_and_get_token(username: str, password: str, db: Session):
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        username=user.username,
        user_id=user.id,
        role=user.role,
        expires_delta=ACCESS_TOKEN_EXPIRE_DELTA,
    )
    # Bearer : Server sẽ không kiểm tra danh tính người gửi, mà chỉ xác minh
    # token có hợp lệ không.
    return {"access_token": token, "token_type": "bearer"}
