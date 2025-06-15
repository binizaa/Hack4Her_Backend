from app.database import get_database

#http://127.0.0.1:8000/exploration/1005
from bson import ObjectId

def get_by_client_id(id_cliente, db_name, collection_name):
    db = get_database(db_name)
    collection = db[collection_name]
    
    result = collection.find_one({"id_cliente": id_cliente})
    
    if result:
        result["_id"] = str(result["_id"]) 
        exploration_data = {
            key: str(value) if isinstance(value, ObjectId) else value
            for key, value in result.items()
        }
        return exploration_data
    else:
        return "No document found with that client_id."

