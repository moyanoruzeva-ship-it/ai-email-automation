from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import os


# Estructura del análisis
class AnalisisEmail(BaseModel):
    categoria: str
    prioridad: str
    sentimiento: str
    respuesta: str


# Cargar la API Key
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


# Leer los emails del archivo
with open("emails_prueba.txt", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()


# Separar los emails
emails = contenido.split("EMAIL ")[1:]


# Analizar cada email
for numero, email in enumerate(emails, start=1):

    # Eliminar el número y espacios sobrantes
    email = email.split("\n", 1)[1].strip()

    print(f"\n========== EMAIL {numero} ==========\n")
    print("Email recibido:")
    print(email)

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

    analisis = resultado.output_parsed

    print("\n--- ANÁLISIS ---")
    print("Categoría:", analisis.categoria)
    print("Prioridad:", analisis.prioridad)
    print("Sentimiento:", analisis.sentimiento)

    print("\n--- RESPUESTA SUGERIDA ---")
    print(analisis.respuesta)
