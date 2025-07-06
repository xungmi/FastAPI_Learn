"""
Dependencies for API routes
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import ALGORITHM, SECRET_KEY

# Import từ app structure
from app.core.database import get_db
from app.models.todo import Todos
from app.models.user import Users

# OAuth2 scheme for token authentication
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


# =============================================================================
# AUTHENTICATION DEPENDENCIES
# =============================================================================


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
    db: Annotated[Session, Depends(get_db)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None or user_role is None:
            raise credentials_exception
        return {"username": username, "id": user_id, "role": user_role}
    except JWTError:
        raise credentials_exception


async def get_current_active_user(
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """
    Check if current user is active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


# =============================================================================
# AUTHORIZATION DEPENDENCIES
# =============================================================================


async def get_current_admin_user(
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """
    Check if current user has admin role
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin role required.",
        )
    return current_user


def require_role(required_role: str):
    """
    Factory function to create role-based dependency
    """

    def check_role(current_user: Annotated[Users, Depends(get_current_user)]):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' required. Current role: '{current_user.role}'",
            )
        return current_user

    return check_role


# =============================================================================
# VALIDATION DEPENDENCIES
# =============================================================================


async def validate_todo_exists(
    todo_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """
    Validate that todo exists and belongs to current user
    """
    todo = (
        db.query(Todos)
        .filter(Todos.id == todo_id, Todos.owner_id == current_user.id)
        .first()
    )

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )
    return todo


async def validate_user_exists(user_id: int, db: Annotated[Session, Depends(get_db)]):
    """
    Validate that user exists
    """
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user


# =============================================================================
# UTILITY DEPENDENCIES
# =============================================================================


def get_pagination_params(skip: int = 0, limit: int = 100):
    """
    Pagination parameters
    """
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Skip must be >= 0"
        )
    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 1000",
        )
    return {"skip": skip, "limit": limit}


# =============================================================================
# RATE LIMITING DEPENDENCIES (Optional)
# =============================================================================

import time
from collections import defaultdict

from fastapi import Request

# Simple in-memory rate limiting (for production, use Redis)
request_counts = defaultdict(list)


def rate_limit(max_requests: int = 100, window_seconds: int = 60):
    """
    Rate limiting dependency
    """

    def check_rate_limit(request: Request):
        client_ip = request.client.host
        current_time = time.time()

        # Clean old requests
        request_counts[client_ip] = [
            req_time
            for req_time in request_counts[client_ip]
            if current_time - req_time < window_seconds
        ]

        # Check if limit exceeded
        if len(request_counts[client_ip]) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {max_requests} requests per {window_seconds} seconds.",
            )

        # Add current request
        request_counts[client_ip].append(current_time)

    return check_rate_limit


# =============================================================================
# EXPORT ALL DEPENDENCIES
# =============================================================================

__all__ = [
    "get_current_user",
    "get_current_active_user",
    "get_current_admin_user",
    "require_role",
    "validate_todo_exists",
    "validate_user_exists",
    "get_pagination_params",
    "rate_limit",
]
