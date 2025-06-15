from fastapi import APIRouter, HTTPException
from typing import List
from datetime import date

from app.models.userCategory import UserCategory
from app.services.data_services import get_by_client_id

router = APIRouter()

# Endpoint para obtener la categoría de un usuario
@router.get("/user-category/{id}")
async def get_user_category(id: int):
    """
    Retorna la categoría de un usuario dado su id.
    """
    user = get_by_client_id(id,"users_db", "clasificaciones")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
