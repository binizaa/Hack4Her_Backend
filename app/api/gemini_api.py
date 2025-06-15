from google import genai
import os
import random
from fastapi import APIRouter, HTTPException

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

def get_tua_message(sentiment: bool):
    """
    Genera un mensaje de Tua basado en un sentimiento de consumo (True para positivo, False para negativo).
    El mensaje tendrá un máximo de 20 palabras y variará cada vez.
    """

    random_number = random.uniform(0.7, 1)

    # --- La personalidad de Tua la guacamaya y la instrucción para variar ---
    persona_instruction = (
        "Eres Tua, una guacamaya colorida, curiosa y muy parlanchina. "
        "Tu objetivo es enviar un mensaje breve y personalizado a una persona sobre su consumo en productos para su tienda de abarrotes. "
        "El mensaje debe enfocarse en animarle a ver sus retos de la semana y ofrecerle una reflexión ligera. "
        "Usa un tono alegre, amigable y un toque de sabiduría natural o ambiental. "
        "Puedes incluir alguna exclamación de guacamaya como '¡Pío! y que incetive a comprar más productos'."
        f"Cambia la temperatura del mensaje a {random_number} "
        "**El mensaje debe tener un máximo de 20 palabras.** "
        "**¡MUY IMPORTANTE: Varia las respuestas cada vez. Que cada mensaje sea diferente y fresco, no repitas frases!**"
    )

    if sentiment: # Si sentimiento es True (positivo)
        sentiment_instruction = (
            "El usuario tiene hábitos de consumo positivos. Felicítale sinceramente. "
            "Anímale a seguir así, resaltando cómo sus decisiones inteligentes en la tienda traen grandes frutos. "
            "Piensa en diferentes formas de expresar 'qué bien' o 'sabiduría' cada vez."
        )
    else: # Si sentimiento es False (negativo)
        sentiment_instruction = (
            "El usuario tiene hábitos de consumo que necesitan un ajuste. "
            "Exprésale tu preocupación de manera amable y constructiva. "
            "Ofrécele una pequeña sugerencia para reflexionar sobre sus 'picotazos' al comprar o la 'cantidad de semillas' que usa. "
            "Piensa en diferentes formas de sugerir 'reflexión' o 'mejora' cada vez."
        )

    # Combina las instrucciones para formar el prompt final
    full_prompt = f"{persona_instruction}\n{sentiment_instruction}\n\nEnvía el mensaje en primera persona como Tua, de forma concisa y cercana."

    # Generate content using the Gemini model
    response = client.models.generate_content(
        model="gemma-3-1b-it",
        contents=full_prompt
    )
    
    return response.text

# http://0.0.0.0:8000/gemini/tua-message/{sentiment_code}
@router.get("/tua-message/{sentiment_code}")
async def get_tua_consumption_message(
    sentiment_code: int # El parámetro de ruta se recibe como un entero
):
    """
    Genera un mensaje de Tua (la guacamaya) sobre el consumo.
    Usa 1 para positivo o 0 para negativo.
    Ejemplo: /gemini/tua-message/1 para positivo, /gemini/tua-message/0 para negativo.
    """
    # Convierte el código numérico a un booleano para la función get_tua_message
    if sentiment_code == 1:
        is_positive = True
    elif sentiment_code == 0:
        is_positive = False
    else:
        # Lanza una excepción si el código no es 0 ni 1
        raise HTTPException(
            status_code=400,
            detail="El parámetro 'sentiment_code' debe ser 1 (positivo) o 0 (negativo)."
        )

    try:
        tua_response = get_tua_message(is_positive) 
        return {"tua_message": tua_response}
    except Exception as e:
        # Registra el error completo para depuración
        print(f"Error generando mensaje de Tua desde el endpoint API: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno al generar el mensaje de Tua: {e}")
