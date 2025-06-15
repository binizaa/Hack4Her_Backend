from fastapi import APIRouter, HTTPException
from typing import List
from datetime import date

from app.models.userCategory import UserCategory

# Datos simulados de actividades (reemplaza con tu base de datos)
user_activity_data = {
    1: [date(2023, 6, 1), date(2023, 6, 3), date(2023, 6, 5)],
    2: [date(2023, 6, 2), date(2023, 6, 4)],
    3: [date(2023, 6, 5)],
}

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

#http://0.0.0.0:8000/users/active-days/{id}
@router.get("/active-days/{user_id}", response_model=int)
async def get_user_active_days(user_id: int):
    """
    Retorna el número de días en los que el usuario estuvo activo.
    """
    active_days = user_activity_data.get(user_id)
    
    if not active_days:
        raise HTTPException(status_code=404, detail="User not found or no active days recorded")
    
    return len(active_days)

