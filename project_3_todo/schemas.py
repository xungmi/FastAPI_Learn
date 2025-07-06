# Đại diện cho dữ liệu vào/ra API
# Dùng ở Request body, Response body

from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Learn FastAPI",
                "description": "So I can build powerful web APIs",
                "priority": 3,
                "complete": False
            }
        }


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


class Token(BaseModel):
    access_token: str
    token_type: str


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)