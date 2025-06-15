from bson import ObjectId
from app.database import get_database

def get_by_client_id(id_cliente, db_name, collection_name):
    # Obtener la base de datos
    db = get_database(db_name)
    collection = db[collection_name]
    
    # Buscar el documento por 'id_cliente'
    result = collection.find_one({"id_cliente": id_cliente})
    
    # Si el documento existe
    if result:
        # Convertir el _id (ObjectId) a string
        result["_id"] = str(result["_id"]) 
        
        # Convertir todos los ObjectId a string dentro del documento
        exploration_data = {
            key: str(value) if isinstance(value, ObjectId) else value
            for key, value in result.items()
        }
        
        # Retornar el diccionario
        return exploration_data
    else:
        # Si no se encuentra el documento, retornar un diccionario vacío o algún otro mensaje adecuado
        return {"message": "No document found with that client_id."}
