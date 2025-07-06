from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.todo import Todos


def get_all_todos_as_admin(user: dict, db: Session):
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed")
    return db.query(Todos).all()


def delete_todo_as_admin(user: dict, todo_id: int, db: Session):
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_model)
    db.commit()
