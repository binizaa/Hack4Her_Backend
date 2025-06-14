# app/main.py

from services.database import db, youtube_collection, close_mongo_connection, get_database


def perform_database_operations():
    """
    Ejemplo de operaciones con la base de datos usando las instancias importadas.
    """
    print("\n--- Realizando operaciones de base de datos ---")

    print("Intentando insertar documento en 'youtube'...")
    document_to_insert = {"name": "Bini", "city": "pune", "source": "main_script"}
    try:
        insert_result = youtube_collection.insert_one(document_to_insert)
        print(f"Documento insertado con ID: {insert_result.inserted_id}")
    except Exception as e:
        print(f"Error al insertar documento: {e}")


# --- Punto de entrada del script ---
if __name__ == "__main__":
    print("Iniciando aplicación Hack4Her Backend desde main.py...")

    try:
        perform_database_operations()

    except Exception as e:
        print(f"Ocurrió un error crítico en la aplicación: {e}")
    finally:
        close_mongo_connection()
        print("Aplicación finalizada y conexión a MongoDB cerrada.")