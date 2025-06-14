from fastapi import APIRouter, HTTPException
from typing import List

from app.models.product_summary_model import ProductQuantity

from app.services.database import db 

router = APIRouter()

@router.get("/product-quantities", response_model=List[ProductQuantity])
async def get_product_quantities():
    """
    Retorna una lista de productos con sus cantidades.
    """
    dummy_data = [
        {"product_name": "Laptop", "quantity": 100},
        {"product_name": "Mouse", "quantity": 250},
        {"product_name": "Teclado", "quantity": 180},
    ]
    return dummy_data