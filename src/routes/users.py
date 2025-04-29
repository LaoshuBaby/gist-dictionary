from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from db import db
from middleware.auth import get_api_key
from models.user import User, UserCreate, UserList, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=UserList)
async def get_users(
    skip: int = 0, 
    limit: int = 100, 
    api_key: str = Depends(get_api_key)
):
    users = db.get_users(skip=skip, limit=limit)
    return {
        "users": users,
        "total": len(db.users),
        "page": skip // limit + 1 if limit > 0 else 1,
        "limit": limit
    }


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: str, 
    api_key: str = Depends(get_api_key)
):
    user = db.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, 
    api_key: str = Depends(get_api_key)
):
    return db.create_user(user)


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: str, 
    user: UserUpdate, 
    api_key: str = Depends(get_api_key)
):
    updated_user = db.update_user(user_id, user)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str, 
    api_key: str = Depends(get_api_key)
):
    success = db.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return None