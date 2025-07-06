from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import Annotated

import models, schemas
from database import SessionLocal


router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

# Dependency mở và đóng kết nối DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBDependency = Annotated[Session, Depends(get_db)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: DBDependency):
    return db.query(models.Todos).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    db: DBDependency,
    todo_id: int = Path(gt=0)
):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: DBDependency, todo_request: schemas.TodoRequest):
    todo_model = models.Todos(**todo_request.dict())
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
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
    
    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    db: DBDependency,
    todo_id: int = Path(gt=0)
):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo_model)
    db.commit()
    