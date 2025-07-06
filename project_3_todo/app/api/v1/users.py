from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import UserVerification
from app.services import user_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


DBDependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: DBDependency):
    return user_service.get_user_by_id(user["id"], db)


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: DBDependency, user_verification: UserVerification
):
    user_service.change_user_password(user["id"], user_verification, db)
