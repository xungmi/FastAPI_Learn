# Đại diện cho dữ liệu vào/ra API
# Dùng ở Request body, Response body


from pydantic import BaseModel, Field


"""
Không khai báo id và is_active vì:
    id: để SQLAlchemy tự sinh.
    is_active: mặc định là True.
"""
# Auth schemas
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)