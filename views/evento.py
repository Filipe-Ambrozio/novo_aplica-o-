import streamlit as st
import urllib.parse
from datetime import datetime


def render():
    st.title("🚨 Evento")

    data = st.date_input("Data", value=datetime.now(), key="evento_data")
    hora = st.text_input("Hora", datetime.now().strftime("%H:%M"), key="evento_hora")

    tipo = st.text_input("Tipo", key="evento_tipo")
    local = st.text_input("Local", key="evento_local")

    ocorrencia = st.text_area("Ocorrência", key="evento_ocorrencia")
    providencias = st.text_area("Providências", key="evento_providencias")

    texto = f"""REGISTRO DE EVENTO

📆 {data.strftime('%d/%m/%y')}
⏰ {hora}

🚨 {tipo}
📍 {local}

📝 {ocorrencia}

📌 {providencias}
"""

    st.text_area("Prévia", texto, height=250, key="evento_preview")

    if st.button("📤 Compartilhar Evento", key="evento_share"):
        link = f"https://api.whatsapp.com/send?text={urllib.parse.quote(texto)}"
        st.markdown(f"[👉 WhatsApp]({link})")
