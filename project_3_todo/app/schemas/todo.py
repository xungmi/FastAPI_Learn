from pydantic import BaseModel, Field


# Dùng để nhận dữ liệu từ client khi tạo/cập nhật todo
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


# Dùng để trả về dữ liệu cho client sau khi đã lưu vào database
class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    complete: bool
    owner_id: int

    class Config:
        from_attributes = True
