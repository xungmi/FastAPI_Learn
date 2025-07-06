from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import Annotated
from ...core.database import get_db
from ...models import todo
from ..deps import get_current_user


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


DBDependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all_todos_admin(user: user_dependency, db: DBDependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed")
    return db.query(todo.Todos).all()



@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_admin(
    user: user_dependency,
    db: DBDependency,
    todo_id: int = Path(gt=0)
):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed")

    todo_model = db.query(todo.Todos).filter(todo.Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_model)
    db.commit()
