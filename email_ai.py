from dotenv import load_dotenv
from openai import OpenAI
import os

# Cargar variables del archivo .env
load_dotenv()

# Crear cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Pregunta que enviaremos a la IA
pregunta = "Escribe un saludo amable para un cliente."

# Llamada al modelo
respuesta = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": pregunta
        }
    ]
)

print(respuesta.choices[0].message.content)