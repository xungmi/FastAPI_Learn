# chỉ xử lý input/output HTTP.
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import admin_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

DBDependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all_todos_admin(user: user_dependency, db: DBDependency):
    return admin_service.get_all_todos_as_admin(user, db)


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_admin(
    user: user_dependency, db: DBDependency, todo_id: int = Path(gt=0)
):
    admin_service.delete_todo_as_admin(user, todo_id, db)
