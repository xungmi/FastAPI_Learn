# Hướng dẫn sử dụng file `deps.py`

## File `deps.py` đã được tạo với cấu trúc phù hợp:

### 📁 **Cấu trúc file:**
```
app/api/deps.py
├── Authentication Dependencies
├── Authorization Dependencies  
├── Validation Dependencies
├── Utility Dependencies
└── Rate Limiting Dependencies
```

### 🔧 **Các dependencies có sẵn:**

#### 1. **Authentication Dependencies**
```python
from app.api.deps import get_current_user, get_current_active_user

@router.get("/profile")
async def get_profile(current_user: Users = Depends(get_current_user)):
    return current_user

@router.get("/active-profile") 
async def get_active_profile(
    current_user: Users = Depends(get_current_active_user)
):
    return current_user
```

#### 2. **Authorization Dependencies**
```python
from app.api.deps import get_current_admin_user, require_role

@router.post("/admin/users")
async def create_user(
    current_admin: Users = Depends(get_current_admin_user)
):
    # Admin only logic
    pass

@router.get("/manager/dashboard")
async def manager_dashboard(
    current_user: Users = Depends(require_role("manager"))
):
    # Manager only logic
    pass
```

#### 3. **Validation Dependencies**
```python
from app.api.deps import validate_todo_exists, validate_user_exists

@router.get("/todos/{todo_id}")
async def get_todo(todo: Todos = Depends(validate_todo_exists)):
    return todo

@router.get("/users/{user_id}")
async def get_user(user: Users = Depends(validate_user_exists)):
    return user
```

#### 4. **Utility Dependencies**
```python
from app.api.deps import get_pagination_params

@router.get("/todos")
async def get_todos(
    pagination: dict = Depends(get_pagination_params)
):
    skip = pagination["skip"]
    limit = pagination["limit"]
    # Logic here
    pass
```

#### 5. **Rate Limiting Dependencies**
```python
from app.api.deps import rate_limit

@router.post("/todos")
async def create_todo(
    _: None = Depends(rate_limit(max_requests=10, window_seconds=60))
):
    # Rate limited logic
    pass
```

## 📋 **Cách sử dụng trong API routes:**

### **Ví dụ 1: Todo CRUD với authentication**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, validate_todo_exists
from app.core.database import get_db
from app.models.user import Users
from app.models.todo import Todos
from app.schemas.todo import TodoRequest, TodoResponse

router = APIRouter()

@router.post("/todos", response_model=TodoResponse)
async def create_todo(
    todo_data: TodoRequest,
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create todo logic
    pass

@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo: Todos = Depends(validate_todo_exists)):
    return todo
```

### **Ví dụ 2: Admin endpoints**
```python
from app.api.deps import get_current_admin_user

@router.get("/admin/users")
async def get_all_users(
    current_admin: Users = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    # Admin only logic
    pass
```

### **Ví dụ 3: Role-based access**
```python
from app.api.deps import require_role

@router.get("/manager/reports")
async def get_manager_reports(
    current_manager: Users = Depends(require_role("manager"))
):
    # Manager only logic
    pass
```

## 🛠️ **Cấu trúc imports:**

### **Trong API routes:**
```python
from app.api.deps import (
    get_current_user,
    get_current_admin_user,
    validate_todo_exists,
    get_pagination_params
)
```

### **Trong main.py:**
```python
from app.api.deps import oauth2_bearer
```

## ✅ **Lợi ích:**

- 🔐 **Security**: Authentication và authorization tập trung
- 🔄 **Reusability**: Tái sử dụng logic chung
- 🧪 **Testability**: Dễ mock và test
- 🛠️ **Maintainability**: Dễ maintain và update
- 📏 **Consistency**: Logic nhất quán across routes

## 🚀 **Sẵn sàng sử dụng:**

File `deps.py` đã được tạo với đầy đủ dependencies cần thiết cho project FastAPI của bạn. Bạn có thể bắt đầu sử dụng ngay trong các API routes! 