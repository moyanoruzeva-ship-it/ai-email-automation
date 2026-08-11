from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import os
import csv
import re


class AnalisisEmail(BaseModel):
    categoria: str
    prioridad: str
    sentimiento: str
    respuesta: str


# Cargar la API Key
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


def analizar_email(remitente, asunto, cuerpo):
    """
    Analiza un email utilizando inteligencia artificial.
    """

    resultado = client.responses.parse(
        model="gpt-5-mini",
        input=f"""
Analiza este email de atención al cliente.

Remitente:
{remitente}

Asunto:
{asunto}

Cuerpo:
{cuerpo}


CLASIFICA EL EMAIL SIGUIENDO EXACTAMENTE ESTAS REGLAS:

CATEGORÍA:

- Pedido: cuando el cliente pregunta por un pedido,
  envío, entrega, retraso o estado de un pedido.

- Consulta: cuando el cliente solamente solicita
  información sobre un producto, precio, disponibilidad
  o características.

- Reclamación: cuando el cliente se queja de un problema,
  producto defectuoso, mal servicio, cobro incorrecto
  o solicita una solución o reembolso.

- Otro: cualquier caso que no encaje en las anteriores.


PRIORIDAD:

- Alta: cuando existe un problema con un pedido,
  retraso, producto defectuoso, reembolso o una situación
  que requiere atención urgente.

- Baja: cuando es una consulta informativa normal
  sin ningún problema.

- Media: situaciones que requieren atención pero no son urgentes.


SENTIMIENTO:

- Positivo: el cliente muestra satisfacción o agradecimiento.

- Neutral: el cliente solicita información sin mostrar
  emociones negativas.

- Negativo: el cliente muestra enfado, frustración,
  decepción o descontento.


IMPORTANTE:

Elige una sola categoría.
Elige una sola prioridad.
Elige un solo sentimiento.

Después genera una respuesta profesional,
clara y amable para el cliente.
""",
        text_format=AnalisisEmail,
    )

    return resultado.output_parsed


# Leer los emails de prueba
with open("emails_prueba.txt", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()


emails = re.split(r"EMAIL\s+\d+", contenido)[1:]

resultados = []


# Procesar cada email
for numero, email in enumerate(emails, start=1):

    lineas = [
        linea.strip()
        for linea in email.strip().splitlines()
        if linea.strip()
    ]

    remitente = lineas[0].replace("De: ", "")
    asunto = lineas[1].replace("Asunto: ", "")
    cuerpo = "\n".join(lineas[2:]).strip()

    print(f"\n========== EMAIL {numero} ==========")
    print("Remitente:", remitente)
    print("Asunto:", asunto)

    analisis = analizar_email(
        remitente,
        asunto,
        cuerpo
    )

    print("\n--- ANÁLISIS ---")
    print("Categoría:", analisis.categoria)
    print("Prioridad:", analisis.prioridad)
    print("Sentimiento:", analisis.sentimiento)

    print("\n--- RESPUESTA SUGERIDA ---")
    print(analisis.respuesta)

    resultados.append({
        "remitente": remitente,
        "asunto": asunto,
        "cuerpo": cuerpo,
        "categoria": analisis.categoria,
        "prioridad": analisis.prioridad,
        "sentimiento": analisis.sentimiento,
        "respuesta": analisis.respuesta
    })


# Guardar resultados
with open(
    "resultados_emails.csv",
    "w",
    newline="",
    encoding="utf-8"
) as archivo:

    campos = [
        "remitente",
        "asunto",
        "cuerpo",
        "categoria",
        "prioridad",
        "sentimiento",
        "respuesta"
    ]

    escritor = csv.DictWriter(
        archivo,
        fieldnames=campos
    )

    escritor.writeheader()
    escritor.writerows(resultados)


print("\n✅ Resultados guardados en resultados_emails.csv")