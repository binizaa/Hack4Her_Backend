from fastapi import APIRouter, HTTPException
from typing import List

from app.models.product_summary_model import ProductQuantity
from app.services.data_services import get_exploration_by_client_id
from app.api.gemini_api import get_product_message

router = APIRouter()

# --- Endpoint para consultar información por id_cliente ---
# http://0.0.0.0:8000/products//exploration/{client_id}
@router.get("/exploration/{client_id}")
async def get_exploration(client_id: int):
    informacion = get_exploration_by_client_id(client_id)
    if informacion:
        
        # Productos en formato JSON
        productos = {
            "cantidad_estimada": informacion["cantidad_estimada"],
            "categoria": informacion["categoria"],
            "producto": informacion["producto"]
        }

        # Frase natural
        frase = get_product_message(productos)
        
        return {"frase": frase, "productos": productos}
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")