# app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
import uvicorn 

# --- Importaciones de tus módulos ---

# from app.services.database import db, youtube_collection, close_mongo_connection, get_database

from app.api import products, user

# Definir los orígenes permitidos
origins = [
    "http://localhost",
    "http://localhost:3000",  # La URL donde se ejecutará tu aplicación React
    "http://127.0.0.1:3000",  # Otra posible URL de desarrollo de React
    # Puedes añadir otras URLs si tu frontend se aloja en otros dominios
]
app = FastAPI(
    title="Hack4Her Backend API",
    description="API para el proyecto Hack4Her",
    version="1.0.0",
)

# --- Configuración de CORS ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,         
    allow_methods=["*"],            
    allow_headers=["*"],            
)

# # --- Eventos de la Aplicación (Startup y Shutdown) ---
# @app.on_event("startup")
# async def startup_event():
#     print("Aplicación iniciando. Verificando conexión a MongoDB...")
#     try:
#         get_database().command('ping') 
#         print("Conexión a MongoDB exitosa en el arranque.")
#     except Exception as e:
#         print(f"ADVERTENCIA: No se pudo conectar a MongoDB al iniciar: {e}")
#         # En producción, podrías querer que la aplicación no inicie si la DB no está disponible.

# @app.on_event("shutdown")
# def shutdown_event():
#     """Cierra la conexión a MongoDB al apagar la aplicación."""
#     close_mongo_connection()
#     print("Aplicación apagándose. Conexión a MongoDB cerrada.")

# --- Inclusión de Routers (Endpoints) ---
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(user.router, prefix="/users", tags=["users"])

# --- Punto de entrada para ejecutar la aplicación con Uvicorn ---
if __name__ == "__main__":
    print("Iniciando servidor Uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=8000)