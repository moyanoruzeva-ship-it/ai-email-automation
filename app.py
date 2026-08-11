import streamlit as st
from email_ai import analizar_email


st.set_page_config(
    page_title="Analizador de Emails con IA",
    page_icon="📧"
)


st.title("📧 Analizador de Emails con IA")
st.write("Analiza automáticamente emails de clientes utilizando inteligencia artificial.")


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
    placeholder="Escribe aquí el contenido del email..."
)


if st.button("🤖 Analizar email"):

    if not cuerpo.strip():
        st.warning("Escribe el contenido del email antes de analizarlo.")

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