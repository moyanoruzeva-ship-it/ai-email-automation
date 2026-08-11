from dotenv import load_dotenv
import os
from openai import OpenAI

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la API Key
api_key = os.getenv("OPENAI_API_KEY")

# Crear el cliente de OpenAI
client = OpenAI(api_key=api_key)

# Hacer una pregunta a la IA
respuesta = client.responses.create(
    model="gpt-5-mini",
    input="Explica en una frase qué es la inteligencia artificial."
)

# Mostrar la respuesta
print(respuesta.output_text)
