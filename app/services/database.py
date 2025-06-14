# app/database.py

from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
# Es buena práctica cargar las variables de entorno al inicio de tu aplicación
# o en cada módulo que las necesite, si están muy separadas.
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

# --- Validaciones y configuración de la conexión ---
if not MONGODB_URI:
    raise ValueError("MONGODB_URI no está definida en el archivo .env. "
                     "Asegúrate de que tu .env contenga MONGODB_URI='mongodb://...'")

try:
    client = MongoClient(MONGODB_URI)

    db = client['db1']

    youtube_collection = db['youtube']

    print("MongoDB client inicializado. Conexión a la base de datos 'db1' lista.")

except Exception as e:
    print(f"ERROR: No se pudo conectar a MongoDB. Revisa tu MONGODB_URI y el estado del servidor. Detalles: {e}")
    client = None 
    db = None

def close_mongo_connection():
    """Cierra la conexión activa a MongoDB."""
    if client:
        client.close()
        print("Conexión a MongoDB cerrada.")

def get_mongo_client():
    """Retorna la instancia global del cliente MongoDB."""
    return client

def get_database():
    """Retorna la instancia global de la base de datos MongoDB."""
    return db