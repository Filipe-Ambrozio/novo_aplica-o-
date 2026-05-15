import streamlit as st
import requests
from datetime import datetime

LOCALS = [
    "BALCÃO DE ATEND. LANCHONETE FRIO (0 a 10°C)",
    "EXPOSITOR DE LATICÍNIOS (0 A 10°C)",
    "ANTECÂMARA - (12° a 18ºC) DELI (15-18ºC)",
    "CÂMARA DOS RESFRIADOS (0 a 10C)",
    "EXPOSITOR DE CARNES (0 A 7°C)",
    "PLANILHA (PAC 04)",
    "EXPOSITOR DOS LATICÍNIOS(QUEIJOS) (0 a 10°C)",
    "SALA DE MANIPULAÇÃO DO AÇOUGUE(15-18ºC)",
    "CÂMARA DO AÇOUGUE ( 0 a 7ºC)",
    "EXPOSITOR DE FRANGOS ( 0 a 4ºC)",
    "CÂMARA DOS CONGELADOS (-12°C OU MAIS FRIO)",
    "BALCÃO. ATEND. LANCHONETE QUENTE (SUPERIOR A 60°C)",
    "DELI (15-18ºC)",
    "EXPOSITOR DA HORTIFRUTI (15 A 18°C)",
    "CÂMARA DOS IMPRÓPRIOS (ATÉ 10ºC)",
    "BALCÃO DE ATENDIMENTO DELI (0 a 10°C)",
    "BALCÃO DOS FATIADOS (0 A 10°C)",
    "SALA DE MANIPULAÇÃO DO HORTFRUTI (15-18ºC)",
]
AREAS = [
    "Freezer 1 - PEIXE",
    "Freezer 2 - FRANGO",
    "Freezer 3 - AVES GERAL",
    "Freezer 2",
    "Geladeira 1",
    "Geladeira 2",
]


def moeda(v):
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def render(URL, nomes):
    st.title("🌡️ Controle de Temperatura")

    nome = st.selectbox("Responsável", nomes, key="temp_nome")
    local = st.selectbox("Local", LOCALS, key="temp_local")

    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.info(data_hora)

    with st.form("form_temp", clear_on_submit=True):
        area = st.selectbox("Área", AREAS, key="temp_area")
        temperatura = st.number_input("Temperatura (°C)", step=0.1, key="temp_temperatura")
        status = st.text_input("Status / Observação", key="temp_status")

        submitted = st.form_submit_button("Adicionar")

        if submitted:
            st.session_state.temp.append(
                {
                    "tipo_registro": "temperatura",
                    "data_hora": data_hora,
                    "nome": nome,
                    "local": local,
                    "area": area,
                    "temperatura": temperatura,
                    "status": status,
                }
            )
            st.success("Adicionado!")

    st.subheader("📋 Lista")

    for i, r in enumerate(st.session_state.temp):
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])

        col1.write(r["local"])
        col2.write(r["area"])
        col3.write(f'{r["temperatura"]} °C')
        col4.write(r["status"])
        col5.write(r["nome"])

        if col6.button("❌", key=f"t{i}"):
            st.session_state.temp.pop(i)
            st.rerun()

    # =========================
    # LOCAIS COM COLETA
    # =========================
    st.subheader("📍 Locais com Coleta")

    locais_coletados = set(r["local"] for r in st.session_state.temp)
    if locais_coletados:
        for local in sorted(locais_coletados):
            st.write(f"✅ {local}")
    else:
        st.write("Nenhum local coletado ainda.")

    if st.button("💾 Salvar", key="temp_salvar"):
        for r in st.session_state.temp:
            requests.post(URL, json=r)

        st.success("Salvo!")
        st.session_state.temp = []
        st.rerun()
