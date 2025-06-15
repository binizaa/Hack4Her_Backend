from fastapi import APIRouter, HTTPException
from typing import List

from app.models.product_summary_model import ProductQuantity
from app.services.data_services import get_by_client_id
from app.api.gemini_api import get_product_message

router = APIRouter()

# --- Endpoint para consultar información por id_cliente ---
#Ejemplo
#http://0.0.0.0:8000/products/volumen/{client_id}
# http://0.0.0.0:8000/products/exploracion/{client_id}
@router.get("/{category}/{client_id}")
async def get_exploration(client_id: int, category: str):
    db_name = f"{category}_db"
    informacion = get_by_client_id(client_id,db_name, "productos_recomendados")
    if informacion:

        name = "Nombre"

        # Frase natural
        frase = get_product_message(informacion, category)
        
        return {"nombre": name, "frase": frase, "productos": informacion}
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
