from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os
import random

# Configurar cliente Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Crear app
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_tua_message(sentiment: bool):
    random_number = random.uniform(0.7, 1)

    persona_instruction = (
        "Eres Tua, una guacamaya colorida, curiosa y muy parlanchina. "
        "Tu objetivo es enviar un mensaje breve y personalizado a una persona sobre su consumo en productos para su tienda de abarrotes. "
        "El mensaje debe enfocarse en animarle a ver sus retos de la semana y ofrecerle una reflexión ligera. "
        "Usa un tono alegre, amigable y un toque de sabiduría natural o ambiental. "
        "Puedes incluir alguna exclamación de guacamaya como '¡Pío!' "
        f"Cambia la temperatura del mensaje a {random_number} "
        "**El mensaje debe tener un máximo de 20 palabras.** "
        "**¡MUY IMPORTANTE: Varia las respuestas cada vez. Que cada mensaje sea diferente y fresco, no repitas frases!**"
    )

    if sentiment:
        sentiment_instruction = (
            "El usuario tiene hábitos de consumo positivos. Felicítale sinceramente. "
            "Anímale a seguir así, resaltando cómo sus decisiones inteligentes en la tienda traen grandes frutos. "
            "Piensa en diferentes formas de expresar 'qué bien' o 'sabiduría' cada vez."
        )
    else:
        sentiment_instruction = (
            "El usuario tiene hábitos de consumo que necesitan un ajuste. "
            "Exprésale tu preocupación de manera amable y constructiva. "
            "Ofrécele una pequeña sugerencia para reflexionar sobre sus 'picotazos' al comprar o la 'cantidad de semillas' que usa. "
            "Piensa en diferentes formas de sugerir 'reflexión' o 'mejora' cada vez."
        )

    full_prompt = f"{persona_instruction}\n{sentiment_instruction}\n\nEnvía el mensaje en primera persona como Tua, de forma concisa y cercana."

    response = client.models.generate_content(
        model="gemma-3-1b-it",
        contents=full_prompt
    )
    
    return response.text

@app.get("/gemini/tua-message/{sentiment_code}")
async def get_tua_consumption_message(sentiment_code: int):
    print(f"Recibida petición: sentiment_code={sentiment_code}")
    
    if sentiment_code == 1:
        is_positive = True
    elif sentiment_code == 0:
        is_positive = False
    else:
        raise HTTPException(
            status_code=400,
            detail="El parámetro 'sentiment_code' debe ser 1 (positivo) o 0 (negativo)."
        )

    try:
        tua_response = get_tua_message(is_positive) 
        print(f"Respuesta generada: {tua_response}")
        return {"tua_message": tua_response}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@app.get("/")
async def root():
    return {"message": "API de Tua funcionando"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)