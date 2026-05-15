import streamlit as st
import pytz
from datetime import datetime
from views import temperatura, paletes, dashboard, gestao, evento, agenda

st.set_page_config(page_title="Sistema Loja", layout="wide")

# URL antigo (publicação anterior sem doGet/dados válidos)
# URL = "https://script.google.com/macros/s/AKfycbz8wNjzEAD8u_3vzqkEdF4CK0ArnWpX4cYtX8mJwneAK2Oj39i_Ks4hjDHCsWIzNSxKJw/exec"
URL = "https://script.google.com/macros/s/AKfycbzB0L6w6cCS1UDxKt8LeGHdFUBkpfZ3jnPHCbQ757NyyU80rm4zYKKEhlgYMfihKUHVHw/exec"

NOMES = [
    "Luiz Claudio",
    "Filipe Ambrozio",
    "Lucia",
    "Gennif Santana",
    "Jhonattan",
    "Gernan",
    "Giovane",
    "Anderson",
    "Kesia",
    "Janaina Fernandes",
    "Sérgio Medeiros",
    "Josenildo Jose",
    "Roni Vicente",
    "Erick",
    "Daniel",
    "Angelo",
    "Alberto",
]

tz = pytz.timezone("America/Sao_Paulo")
data_hora = datetime.now(tz)

st.sidebar.title("📌 Navegação")
menu = st.sidebar.radio(
    "Menu",
    [
        "🌡️ Temperatura",
        "📦 Paletes",
        "📦\u200bPaleteria",
        "📊 Dashboard",
        "📊 Gestão Diária",
        "🚨 Registro de Evento",
        "📅 Agenda",
    ],
)

hora = st.text_input("⏰ Horário", datetime.now().strftime("%H:%M"), key="hora_global")

if "temp" not in st.session_state:
    st.session_state.temp = []

if "palete" not in st.session_state:
    st.session_state.palete = []

if menu == "🌡️ Temperatura":
    temperatura.render(URL, NOMES)
elif menu in ["📦 Paletes", "📦\u200bPaleteria"]:
    paletes.render(URL, NOMES)
elif menu == "📊 Dashboard":
    dashboard.render()
elif menu == "📊 Gestão Diária":
    gestao.render()
elif menu == "🚨 Registro de Evento":
    evento.render()
elif menu == "📅 Agenda":
    agenda.render(URL)

#streamlit run app.py