from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.todo import TodoRequest
from app.services import todo_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])


DBDependency = Annotated[Session, Depends(get_db)]


"""
dict : là kiểu dữ liệu trả về mong muốn, 
       chứa thông tin người dùng hiện tại, được lấy từ token JWT.
"""
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: DBDependency, user: user_dependency):
    return todo_service.get_all_todos(db, user["id"])


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: DBDependency, user: user_dependency, todo_id: int = Path(gt=0)):
    return todo_service.get_todo_by_id(db, user["id"], todo_id)


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    db: DBDependency, todo_request: TodoRequest, user: user_dependency
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
    return todo_service.create_todo(db, user["id"], todo_request)


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: DBDependency,
    user: user_dependency,
    todo_id: int = Path(gt=0),
    todo_request: TodoRequest = Depends(),
):
    todo_service.update_todo(db, user["id"], todo_id, todo_request)


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    db: DBDependency, user: user_dependency, todo_id: int = Path(gt=0)
):
    todo_service.delete_todo(db, user["id"], todo_id)
