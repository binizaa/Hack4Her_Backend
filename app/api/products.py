from fastapi import APIRouter, HTTPException
from typing import List

from app.models.product_summary_model import ProductQuantity
from app.services.data_services import get_exploration_by_client_id

router = APIRouter()

# http://0.0.0.0:8000/products/product-quantities
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

# --- Endpoint para consultar información por id_cliente ---
# http://0.0.0.0:8000/products//exploration/{client_id}
@router.get("/exploration/{client_id}")
async def get_exploration(client_id: int):
    informacion = get_exploration_by_client_id(client_id)
    if informacion:
        return informacion
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")