# app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Para manejar CORS con tu frontend Next.js
import uvicorn # Para ejecutar la aplicación FastAPI

# --- Importaciones de tus módulos ---
# Asegúrate de que las rutas de importación sean correctas según tu estructura:
# Por ejemplo, si database.py está en app/services/
from app.services.database import db, youtube_collection, close_mongo_connection, get_database

# Importa tus routers de la API. Asegúrate de que estos archivos existan en app/api/
from app.api import products # Este es el router que definimos para las cantidades de productos
# Si tienes otros routers como auth, users, gemini, asegúrate de importarlos también:
# from app.api import auth, users, gemini, health

# --- Inicialización de la aplicación FastAPI ---
app = FastAPI(
    title="Hack4Her Backend API",
    description="API para el proyecto Hack4Her",
    version="1.0.0",
)

# --- Configuración de CORS ---
# Esto es CRUCIAL para que tu frontend Next.js pueda comunicarse con tu backend.
# Reemplaza "http://localhost:3000" con la URL de tu frontend Next.js en desarrollo
# y luego con el dominio de tu frontend en producción.
origins = [
    "http://localhost:3000",  # Frontend de Next.js en desarrollo
    # Agrega más orígenes si tu frontend se ejecuta en otros puertos o dominios
    # "https://your-production-frontend.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Lista de orígenes permitidos
    allow_credentials=True,         # Permitir cookies/credenciales
    allow_methods=["*"],            # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],            # Permitir todos los encabezados
)

# --- Eventos de la Aplicación (Startup y Shutdown) ---
@app.on_event("startup")
async def startup_event():
    print("Aplicación iniciando. Verificando conexión a MongoDB...")
    # Opcional: una prueba de conexión al iniciar
    try:
        get_database().command('ping') # Intenta un ping para verificar la conexión
        print("Conexión a MongoDB exitosa en el arranque.")
    except Exception as e:
        print(f"ADVERTENCIA: No se pudo conectar a MongoDB al iniciar: {e}")
        # En producción, podrías querer que la aplicación no inicie si la DB no está disponible.

@app.on_event("shutdown")
def shutdown_event():
    """Cierra la conexión a MongoDB al apagar la aplicación."""
    close_mongo_connection()
    print("Aplicación apagándose. Conexión a MongoDB cerrada.")

# --- Inclusión de Routers (Endpoints) ---
# Aquí incluyes todos los "routers" definidos en tu carpeta 'app/api/'
app.include_router(products.router, prefix="/products", tags=["Products"])
# Si tienes más routers, inclúyelos aquí:
# app.include_router(auth.router, prefix="/auth", tags=["Auth"])
# app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(gemini.router, prefix="/gemini", tags=["Gemini AI"])
# app.include_router(health.router, prefix="/health", tags=["Health Check"])


# --- Ruta de ejemplo para probar la raíz de la API ---
@app.get("/")
async def read_root():
    return {"message": "Welcome to Hack4Her Backend API! Visit /docs for OpenAPI spec."}

# --- Ruta de prueba para operaciones de base de datos (Opcional) ---
# Esta ruta es un ejemplo de cómo integrar operaciones de DB en un endpoint.
# No es recomendable ejecutar perform_database_operations directamente en __main__
# de una API, a menos que sea un script de inicialización/migración.
@app.post("/test-db-insert")
async def test_db_insert_endpoint():
    """
    Endpoint para probar la inserción de un documento en la colección 'youtube'.
    """
    print("\n--- Endpoint de prueba: Realizando inserción en DB ---")
    document_to_insert = {"name": "TestUser", "city": "TestCity", "source": "api_endpoint"}
    try:
        insert_result = youtube_collection.insert_one(document_to_insert)
        print(f"Documento insertado con ID: {insert_result.inserted_id}")
        return {"message": "Documento insertado correctamente", "id": str(insert_result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar documento: {e}")


# --- Punto de entrada para ejecutar la aplicación con Uvicorn ---
if __name__ == "__main__":
    print("Iniciando servidor Uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # Host "0.0.0.0" permite que la app sea accesible desde otras máquinas en la red local.
    # El puerto 8000 es el puerto estándar para APIs en desarrollo.