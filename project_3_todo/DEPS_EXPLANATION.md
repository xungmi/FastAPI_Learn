# File `deps.py` - Dependencies trong FastAPI

## File `deps.py` chứa gì?

File `deps.py` (dependencies) chứa các **dependency injection functions** được sử dụng trong FastAPI routes. Đây là nơi tập trung các logic chung được tái sử dụng nhiều lần.

## Cấu trúc file `deps.py`:

```python
"""
Dependencies for API routes
"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password
from app.models.user import User
from app.api.v1.auth import oauth2_bearer
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM

async def get_current_user(
    token: str = Depends(oauth2_bearer),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
```

## Các loại dependencies thường có:

### 1. **Authentication Dependencies**
```python
async def get_current_user(token: str = Depends(oauth2_bearer)):
    # Validate JWT token
    # Return current user
    pass

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

### 2. **Authorization Dependencies**
```python
async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions"
        )
    return current_user

async def require_role(required_role: str):
    def check_role(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"Role {required_role} required"
            )
        return current_user
    return check_role
```

### 3. **Database Dependencies**
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_db_session():
    async with async_session() as session:
        yield session
```

### 4. **Validation Dependencies**
```python
async def validate_todo_exists(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.owner_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )
    return todo
```

### 5. **Rate Limiting Dependencies**
```python
from fastapi import Request
import time

def rate_limit(max_requests: int = 100, window_seconds: int = 60):
    def check_rate_limit(request: Request):
        # Implement rate limiting logic
        pass
    return check_rate_limit
```

## Cách sử dụng dependencies:

### **Trong API routes:**
```python
from app.api.deps import get_current_user, get_current_admin_user

@router.get("/todos")
async def get_todos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Logic here
    pass

@router.post("/admin/users")
async def create_user(
    current_admin: User = Depends(get_current_admin_user),
    user_data: CreateUserRequest
):
    # Admin only logic
    pass
```

### **Dependencies với parameters:**
```python
@router.get("/todos/{todo_id}")
async def get_todo(
    todo: Todo = Depends(validate_todo_exists)
):
    return todo

@router.post("/todos")
async def create_todo(
    current_user: User = Depends(get_current_user),
    todo_data: TodoRequest = Depends(validate_todo_data)
):
    # Create todo logic
    pass
```

## Lợi ích của file `deps.py`:

### ✅ **Code Reusability**
- Tái sử dụng logic authentication
- Tái sử dụng database connections
- Tái sử dụng validation logic

### ✅ **Separation of Concerns**
- Logic authentication tách riêng
- Logic authorization tách riêng
- Logic validation tách riêng

### ✅ **Testability**
- Dễ mock dependencies trong tests
- Dễ test từng dependency riêng biệt
- Dễ override dependencies

### ✅ **Maintainability**
- Tập trung logic chung ở một nơi
- Dễ thay đổi logic authentication
- Dễ thêm new dependencies

## Ví dụ thực tế:

### **Authentication Flow:**
```python
# 1. User gửi request với Bearer token
# 2. FastAPI tự động gọi get_current_user()
# 3. get_current_user() validate JWT token
# 4. Trả về user object hoặc raise exception
# 5. Route handler nhận user object
```

### **Authorization Flow:**
```python
# 1. get_current_user() trả về user
# 2. get_current_admin_user() check role
# 3. Nếu role != "admin" → raise 403
# 4. Nếu role == "admin" → trả về user
# 5. Route handler nhận admin user
```

## Best Practices:

### ✅ **Nên làm:**
- Tách riêng authentication và authorization
- Sử dụng type hints
- Handle exceptions properly
- Log important events
- Cache expensive operations

### ❌ **Không nên làm:**
- Mix business logic trong dependencies
- Hardcode values
- Ignore error handling
- Create circular dependencies
- Over-complicate simple logic

## Kết luận:

File `deps.py` là **trung tâm của dependency injection** trong FastAPI, chứa:

- 🔐 **Authentication logic**
- 🛡️ **Authorization logic** 
- 🗄️ **Database connections**
- ✅ **Validation logic**
- ⚡ **Rate limiting**
- 🔄 **Reusable functions**

Đây là pattern chuẩn trong FastAPI để tạo ra code clean, maintainable và testable! 