import csv
from pymongo import MongoClient
import os

# Configuración desde variables de entorno
# Es altamente recomendable usar variables de entorno para las credenciales.
# Si estás ejecutando esto localmente, puedes definir MONGODB_URI en tu shell
# export MONGODB_URI="mongodb+srv://binizarz:vUopdTEx4e7MK4f5@cluster0.oqbmpew.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_URI = os.getenv("MONGODB_URI", "mongodb+srv://binizarz:vUopdTEx4e7MK4f5@cluster0.oqbmpew.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = "users_db"  # Nombre de tu base de datos en MongoDB
COLLECTION_NAME = "clasificaciones" # Nombre de la colección donde se insertarán los datos (MODIFICADO)

# Ruta al archivo CSV
csv_file_path = "clasificacion.csv"  # ¡MODIFICADO para que coincida con la imagen!

# Conexión a MongoDB Atlas con SSL
# tlsAllowInvalidCertificates=False es una buena práctica para producción.
# Si tienes problemas con el certificado en desarrollo, puedes probar a cambiarlo a True TEMPORALMENTE,
# pero siempre busca una solución más segura para producción.
try:
    client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=False)
    # The ping command is cheap and does not require auth.
    client.admin.command('ping')
    print("Conexión a MongoDB exitosa!")
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")
    exit() # Salir si no se puede conectar a la base de datos

db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Borrar colección existente (opcional, para evitar duplicados en cada ejecución)
print(f"Borrando documentos existentes en la colección '{COLLECTION_NAME}'...")
delete_result = collection.delete_many({})
print(f"{delete_result.deleted_count} documentos eliminados.")

# Procesar archivo CSV
total_docs = 0
lineas_procesadas = 0
lineas_con_errores = 0

try:
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Opcional: Verificar que las columnas esperadas existan en el CSV (MODIFICADO)
        expected_headers = ['ID Cliente', 'meses_consecutivos', 'Categoria']
        if not all(header in reader.fieldnames for header in expected_headers):
            print(f"Error: El archivo CSV no contiene todas las columnas esperadas. Columnas encontradas: {reader.fieldnames}")
            print(f"Columnas esperadas: {expected_headers}")
            client.close()
            exit()

        for row in reader:
            lineas_procesadas += 1
            try:
                # Mapeo de columnas del CSV a campos del documento MongoDB (MODIFICADO)
                doc = {
                    'id_cliente': int(row['ID Cliente']),
                    'meses_consecutivos': int(row['meses_consecutivos']),
                    'categoria': row['Categoria'].strip() if row.get('Categoria') else None
                }
                
                # Insertar documento
                collection.insert_one(doc)
                total_docs += 1
            except ValueError as ve:
                print(f"Error de valor en la línea {lineas_procesadas}: {row} - {ve}. Saltando esta línea.")
                lineas_con_errores += 1
            except KeyError as ke:
                print(f"Error de columna faltante en la línea {lineas_procesadas}: {row} - {ke}. Saltando esta línea.")
                lineas_con_errores += 1
            except Exception as e:
                print(f"Error inesperado en la línea {lineas_procesadas}: {row} - {e}. Saltando esta línea.")
                lineas_con_errores += 1

except FileNotFoundError:
    print(f"Error: El archivo '{csv_file_path}' no se encontró. Asegúrate de que esté en la misma carpeta que el script o proporciona la ruta completa.")
    client.close()
    exit()
except Exception as e:
    print(f"Error general al leer el archivo CSV: {e}")
    client.close()
    exit()


# Estadísticas finales
print(f"\n✅ Carga completada:")
print(f"- Líneas del CSV procesadas: {lineas_procesadas}")
print(f"- Documentos insertados exitosamente: {total_docs}")
print(f"- Líneas con errores (no insertadas): {lineas_con_errores}")
print(f"- Documentos actuales en la colección '{COLLECTION_NAME}': {collection.count_documents({})}")

# Verificar conexión
print("\n💾 Configuración de MongoDB:")
print(f"- Servidor: {client.HOST}:{client.PORT}")
print(f"- Base de datos: {DB_NAME}")
print(f"- Colección: {COLLECTION_NAME}")

# Cerrar conexión
client.close()
print("Conexión a MongoDB cerrada.")