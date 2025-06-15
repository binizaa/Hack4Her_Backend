from app.database import get_database

#http://127.0.0.1:8000/exploration/1005
def get_exploration_by_client_id(id_cliente):
    db = get_database("exploracion_db")
    collection = db["productos_recomendados"]
    
    # Buscar el documento con el id_cliente
    result = collection.find_one({"id_cliente": id_cliente})
    
    if result:
        # Extraer los campos específicos
        exploration_data = {
            "cantidad_estimada": result.get("cantidad_estimada"),
            "categoria": result.get("categoria"),
            "producto": result.get("producto")
        }
        return exploration_data
    else:
        return "No document found with that client_id."
