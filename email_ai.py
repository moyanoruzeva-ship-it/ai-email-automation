from dotenv import load_dotenv
import os
from openai import OpenAI

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la API Key
api_key = os.getenv("OPENAI_API_KEY")

# Crear el cliente de OpenAI
client = OpenAI(api_key=api_key)

# Email de prueba
email = """
Hola,

Hice un pedido hace una semana y todavía no lo he recibido.
¿Podrían decirme cuándo llegará?

Gracias.
"""

# Pedir a la IA que analice el email
respuesta = client.responses.create(
    model="gpt-5-mini",
    input=f"""
Analiza el siguiente email de un cliente.

Indica:
1. Categoría del email: Pedido, Consulta, Reclamación u Otro.
2. Prioridad: Baja, Media o Alta.
3. Sentimiento: Positivo, Neutral o Negativo.
4. Escribe una respuesta profesional y amable para el cliente.

Email:
{email}
"""
)

# Mostrar el resultado
print("\n--- ANÁLISIS DEL EMAIL ---\n")
print(respuesta.output_text)
