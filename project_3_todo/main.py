from fastapi import FastAPI
from database import engine
import models
from routers import auth, todos
from routers import admin


# Tạo bảng nếu chưa có
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Đăng ký các router
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)