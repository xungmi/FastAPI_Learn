from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.todo import Todos
from app.schemas.todo import TodoRequest


def get_all_todos(db: Session, user_id: int):
    return db.query(Todos).filter(Todos.owner_id == user_id).all()


def get_todo_by_id(db: Session, user_id: int, todo_id: int):
    todo = (
        db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user_id).first()
    )
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


def create_todo(db: Session, user_id: int, todo_data: TodoRequest):
    todo_model = Todos(**todo_data.dict(), owner_id=user_id)
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


def update_todo(db: Session, user_id: int, todo_id: int, todo_data: TodoRequest):
    todo = get_todo_by_id(db, user_id, todo_id)
    for key, value in todo_data.dict().items():
        setattr(todo, key, value)
    db.commit()
    return todo


def delete_todo(db: Session, user_id: int, todo_id: int):
    todo = get_todo_by_id(db, user_id, todo_id)
    db.delete(todo)
    db.commit()
