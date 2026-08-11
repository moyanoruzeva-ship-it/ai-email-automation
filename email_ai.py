from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import os
import csv


class AnalisisEmail(BaseModel):
    categoria: str
    prioridad: str
    sentimiento: str
    respuesta: str


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


with open("emails_prueba.txt", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()


emails = contenido.split("EMAIL ")[1:]

resultados = []


for numero, email in enumerate(emails, start=1):

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

    resultados.append({
        "email": email,
        "categoria": analisis.categoria,
        "prioridad": analisis.prioridad,
        "sentimiento": analisis.sentimiento,
        "respuesta": analisis.respuesta
    })


with open("resultados_emails.csv", "w", newline="", encoding="utf-8") as archivo:

    campos = [
        "email",
        "categoria",
        "prioridad",
        "sentimiento",
        "respuesta"
    ]

    escritor = csv.DictWriter(archivo, fieldnames=campos)

    escritor.writeheader()
    escritor.writerows(resultados)


print("\n✅ Resultados guardados en resultados_emails.csv")
