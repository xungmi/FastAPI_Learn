from fastapi import FastAPI
from .api.v1 import admin, auth
from .core.database import engine
from .core.database import Base
from .api.v1 import todos, users, auth, admin


# Tạo bảng nếu chưa có
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Đăng ký các router
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)