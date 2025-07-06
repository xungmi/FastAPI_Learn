from fastapi import FastAPI

from app.api.v1 import admin, auth, todos, users
from app.core.database import Base, engine

# Tạo bảng nếu chưa có
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Đăng ký các router
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


# api to check the first api testing
@app.get("/healthy")
def health_check():
    return {"status": "healthy"}
