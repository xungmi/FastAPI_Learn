from fastapi import FastAPI, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import Annotated

from database import SessionLocal, engine
import models, schemas
from routers import auth


"""
Kiểm tra các bảng được định nghĩa trong models.py
Tạo bảng tương ứng trong cơ sở dữ liệu todos.db (nếu chưa tồn tại),
dùng engine từ database.py
"""
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(auth.router)


# Dependency mở và đóng kết nối DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBDependency = Annotated[Session, Depends(get_db)]


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: DBDependency):
    return db.query(models.Todos).all()


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    db: DBDependency,
    todo_id: int = Path(gt=0)
):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: DBDependency, todo_request: schemas.TodoRequest):
    todo_model = models.Todos(**todo_request.dict())
    db.add(todo_model)
    db.commit()


@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: DBDependency,
    todo_id: int = Path(gt=0),
    todo_request: schemas.TodoRequest = Depends()
):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    for key, value in todo_request.dict().items():
        setattr(todo_model, key, value)
    
    db.add(todo_model) # để session theo dõi todo_model này => 
        # commit thì SQLAlchemy biết là cần cập nhật bản ghi này trong database.
    db.commit()


@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    db: DBDependency,
    todo_id: int = Path(gt=0)
):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo_model)
    db.commit()
