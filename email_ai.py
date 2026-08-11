from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import os


# Estructura que queremos recibir de la IA
class AnalisisEmail(BaseModel):
    categoria: str
    prioridad: str
    sentimiento: str
    respuesta: str


# Cargar variables del archivo .env
load_dotenv()

# Obtener API Key
api_key = os.getenv("OPENAI_API_KEY")

# Crear cliente
client = OpenAI(api_key=api_key)


# Pedir un email al usuario
email = input("Introduce el email del cliente:\n")


# Analizar el email
resultado = client.responses.parse(
    model="gpt-5-mini",
    input=f"""
Analiza el siguiente email de un cliente.

Clasifica el email utilizando estas categorías:

- Pedido
- Consulta
- Reclamación
- Otro

La prioridad debe ser:

- Baja
- Media
- Alta

El sentimiento debe ser:

- Positivo
- Neutral
- Negativo

Después escribe una respuesta profesional, clara y amable.

Email del cliente:
{email}
""",
    text_format=AnalisisEmail,
)


# Mostrar resultados
print("\n--- ANÁLISIS DEL EMAIL ---\n")
print("Categoría:", resultado.output_parsed.categoria)
print("Prioridad:", resultado.output_parsed.prioridad)
print("Sentimiento:", resultado.output_parsed.sentimiento)

print("\n--- RESPUESTA SUGERIDA ---\n")
print(resultado.output_parsed.respuesta)
