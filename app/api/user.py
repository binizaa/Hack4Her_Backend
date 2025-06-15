from fastapi import APIRouter, HTTPException
from typing import List

from app.models.userCategory import UserCategory

dummy_users = {
    1: "admin",
    2: "moderator",
    3: "user"
}

router = APIRouter()

# http://0.0.0.0:8000/users/user-category/{id}
@router.get("/user-category/{id}", response_model=UserCategory)
async def get_user_category(id: int):
    """
    Retorna la categoría de un usuario dado su id.
    """
    category = dummy_users.get(id)
    if category is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserCategory(category=category)
