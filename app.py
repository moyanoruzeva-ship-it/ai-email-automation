import streamlit as st
from email_ai import analizar_email
import csv
import os


st.set_page_config(
    page_title="Analizador de Emails con IA",
    page_icon="📧"
)

st.title("📧 Analizador de Emails con IA")
st.write(
    "Analiza automáticamente correos electrónicos de clientes "
    "utilizando inteligencia artificial."
)


remitente = st.text_input(
    "Remitente",
    placeholder="cliente@email.com"
)

asunto = st.text_input(
    "Asunto",
    placeholder="Pedido retrasado"
)

cuerpo = st.text_area(
    "Email del cliente",
    height=200,
    placeholder="Escribe aquí el contenido del correo electrónico..."
)


if st.button("🤖 Analizar correo electrónico"):

    if not cuerpo.strip():
        st.warning("Escribe el contenido del correo antes de analizarlo.")

    else:

        with st.spinner("Analizando el email con IA..."):

            analisis = analizar_email(
                remitente,
                asunto,
                cuerpo
            )

        st.subheader("📊 Análisis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Categoría", analisis.categoria)

        with col2:
            st.metric("Prioridad", analisis.prioridad)

        with col3:
            st.metric("Sentimiento", analisis.sentimiento)

        st.subheader("✍️ Respuesta sugerida")

        st.write(analisis.respuesta)


        # Guardar el resultado en CSV

        archivo_csv = "resultados_emails.csv"

        campos = [
            "remitente",
            "asunto",
            "cuerpo",
            "categoria",
            "prioridad",
            "sentimiento",
            "respuesta"
        ]

        existe_archivo = os.path.exists(archivo_csv)
        archivo_vacio = (
            not existe_archivo
            or os.path.getsize(archivo_csv) == 0
        )

        with open(
            archivo_csv,
            "a",
            newline="",
            encoding="utf-8"
        ) as archivo:

            escritor = csv.DictWriter(
                archivo,
                fieldnames=campos
            )

            if archivo_vacio:
                escritor.writeheader()

            escritor.writerow({
                "remitente": remitente,
                "asunto": asunto,
                "cuerpo": cuerpo,
                "categoria": analisis.categoria,
                "prioridad": analisis.prioridad,
                "sentimiento": analisis.sentimiento,
                "respuesta": analisis.respuesta
            })

        st.success("✅ Análisis guardado en resultados_emails.csv")