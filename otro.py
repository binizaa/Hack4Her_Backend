import csv
from pymongo import MongoClient
from io import StringIO
import os

# Configuración desde variables de entorno
MONGO_URI = os.getenv("MONGODB_URI", "mongodb+srv://binizarz:vUopdTEx4e7MK4f5@cluster0.oqbmpew.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = "exploracion_db"
COLLECTION_NAME = "productos_recomendados"

# Ruta al archivo CSV
csv_file_path = "exploración.csv"  # Ajusta la ruta según corresponda

# Conexión a MongoDB Atlas con SSL
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=False)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Borrar colección existente (opcional)
collection.delete_many({})

# Procesar archivo CSV
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    # Contadores para estadísticas
    total_docs = 0
    lineas_incompletas = 0

    for row in reader:
        # Manejar líneas incompletas
        if not row.get('Producto Recomendado Nombre', '').strip():
            row['Producto Recomendado Nombre'] = None
            lineas_incompletas += 1
        
        # Crear documento
        doc = {
            'id_cliente': int(row['ID Cliente']),
            'cantidad_estimada': float(row['Cantidad Estimada (cajas)']),
            'categoria': row['Categoría Recomendada Nombre'],
            'producto': row['Producto Recomendado Nombre']
        }
        
        # Insertar documento
        collection.insert_one(doc)
        total_docs += 1

# Estadísticas finales
print(f"\n✅ Carga completada:")
print(f"- Documentos insertados: {total_docs}")
print(f"- Líneas incompletas procesadas: {lineas_incompletas}")
print(f"- Documentos en colección: {collection.count_documents({})}")

# Verificar conexión
print("\n💾 Configuración de MongoDB:")
print(f"- Servidor: {client.HOST}:{client.PORT}")
print(f"- Base de datos: {DB_NAME}")
print(f"- Colección: {COLLECTION_NAME}")

# Cerrar conexión
client.close()
