# Cấu trúc tổ chức code FastAPI

## Tổ chức file theo chức năng

### 1. `models.py` - Database Models
- Chứa các SQLAlchemy models
- Đại diện cho cấu trúc database tables
- Ví dụ: `Users`, `Todos`

### 2. `schemas.py` - API Schemas  
- Chứa các Pydantic BaseModel
- Đại diện cho Request/Response data của API
- Bao gồm:
  - `TodoRequest`: Schema cho todo operations
  - `CreateUserRequest`: Schema cho user registration
  - `Token`: Schema cho authentication response

### 3. `routers/auth.py` - Authentication Logic
- Chứa logic xử lý authentication
- Import schemas từ `schemas.py`
- Không định nghĩa BaseModel classes

## Lý do tổ chức như vậy

### ✅ **Tính nhất quán**
- Tất cả schemas ở một nơi (`schemas.py`)
- Dễ tìm và maintain

### ✅ **Separation of Concerns**
- `models.py`: Database entities
- `schemas.py`: API data validation
- `auth.py`: Business logic

### ✅ **Dễ mở rộng**
- Thêm schema mới chỉ cần vào `schemas.py`
- Không cần sửa nhiều file

### ✅ **Best Practices**
- Tuân theo FastAPI conventions
- Code dễ đọc và hiểu

## Import pattern
```python
# Trong routers
from schemas import CreateUserRequest, Token
from models import Users
```

## Cấu trúc thư mục
```
project_3_todo/
├── models.py      # Database models
├── schemas.py     # API schemas  
├── routers/
│   ├── auth.py    # Auth logic
│   └── todos.py   # Todo logic
└── main.py        # App entry point
``` 