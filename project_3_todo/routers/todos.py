from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import Annotated

import models, schemas
from database import get_db

from .auth import get_current_user


router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)


DBDependency = Annotated[Session, Depends(get_db)]


"""
dict : là kiểu dữ liệu trả về mong muốn, 
       chứa thông tin người dùng hiện tại, được lấy từ token JWT.
"""
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: DBDependency, user: user_dependency):
    return db.query(models.Todos).filter(models.Todos.owner_id == user["id"]).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    db: DBDependency,
    user: user_dependency,
    todo_id: int = Path(gt=0)
):
    todo_model = db.query(models.Todos).filter(
        models.Todos.id == todo_id,
        models.Todos.owner_id == user["id"]
    ).first()
    if todo_model:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    db: DBDependency,
    todo_request: schemas.TodoRequest,
    user: user_dependency
):
    # if user is None:
    #     raise HTTPException(status_code=401, detail="Authentication failed")
    #  => Đã được kiểm tra trong get_current_user bởi Depend
    # if todo_request is None:
    #     raise HTTPException(status_code=400, detail="Invalid request data")
    #  => pydantic sẽ tự động kiểm tra dữ liệu đầu vào  
    # if not todo_request.title:
    #     raise HTTPException(status_code=400, detail="Title is required")
    #  => pydantic sẽ tự động kiểm tra dữ liệu đầu vào

    todo_model = models.Todos(
        **todo_request.dict(),
        owner_id=user["id"]
    )
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: DBDependency,
    user: user_dependency,
    todo_id: int = Path(gt=0),
    todo_request: schemas.TodoRequest = Depends()
):
    todo_model = db.query(models.Todos).filter(
        models.Todos.id == todo_id,
        models.Todos.owner_id == user["id"]
    ).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    for key, value in todo_request.dict().items():
        setattr(todo_model, key, value)
    
    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    db: DBDependency,
    user: user_dependency,
    todo_id: int = Path(gt=0)
):
    todo_model = db.query(models.Todos).filter(
        models.Todos.id == todo_id,
        models.Todos.owner_id == user["id"]
    ).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo_model)
    db.commit()
    