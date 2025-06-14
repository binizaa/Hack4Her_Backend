from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemma-3-1b-it",
    contents="Why is the sky blue?"
)

print(response.text)