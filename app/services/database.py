from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URI de MongoDB desde las variables de entorno
MONGODB_URI = os.getenv('MONGODB_URI')

# Crear una instancia del cliente de MongoDB
client = MongoClient(MONGODB_URI)

# Especifica explícitamente la base de datos
# Reemplaza 'mydatabase' por el nombre de tu base de datos
db = client['mydatabase']  # Aquí debes poner el nombre de la base de datos que usas

# Cerrar la conexión
def close_mongo_connection():
    client.close()

# Si necesitas exportar otras funciones o colecciones
def get_database():
    return db
