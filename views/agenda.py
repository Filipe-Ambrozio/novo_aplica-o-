import streamlit as st
from datetime import datetime
import urllib.parse
import requests

DEFAULT_AGENDA = [
    {
        "id": 1,
        "data": "2026-05-01",
        "evento": "Inventario não contavel",
        "status": "Finalizado",
        "observacao": "Tratativa",
    },
    {
        "id": 2,
        "data": "2026-05-03",
        "evento": "Reunião de reciclagem",
        "status": "Aberto",
        "observacao": "Reunião com os colaboradore para traigem de abordagem",
    },
    {
        "id": 3,
        "data": "2026-05-20",
        "evento": "Inventario Acougue",
        "status": "Aberto",
        "observacao": "Inventario de acougue parcial",
    },
    {
        "id": 4,
        "data": "2026-05-25",
        "evento": "Final ferias (Nome)",
        "status": "Aberto",
        "observacao": "Terminou das ferias",
    },
    {
        "id": 5,
        "data": "2026-05-25",
        "evento": "Teste de alarme",
        "status": "Aberto",
        "observacao": "Será realizado teste de alarme com o grupo segue.",
    },
]


def normalize_agenda_date(value):
    text = str(value or "").strip()
    if not text:
        return ""

    # Already in yyyy-mm-dd
    if text.count("-") == 2:
        parts = text.split("-")
        if len(parts[0]) == 4 and len(parts[1]) <= 2 and len(parts[2]) <= 2:
            return text

    # Accept dd/mm/yyyy, dd-mm-yyyy, dd.mm.yyyy
    for sep in ["/", "-", "."]:
        if sep in text:
            parts = text.split(sep)
            if len(parts) == 3:
                a, b, c = parts
                if len(c) == 4:
                    if len(a) == 4:
                        return f"{a.zfill(4)}-{b.zfill(2)}-{c.zfill(2)}"
                    return f"{c.zfill(4)}-{b.zfill(2)}-{a.zfill(2)}"

    # Accept ddmmyyyy
    if len(text) == 8 and text.isdigit():
        return f"{text[4:8]}-{text[2:4]}-{text[0:2]}"

    return text


def normalize_status(text):
    return str(text or "").strip().lower()


def load_agenda_events(URL):
    try:
        response = requests.get(
            URL,
            params={"tipo_registro": "agenda", "_ts": str(datetime.now().timestamp())},
            headers={"Cache-Control": "no-cache"},
            timeout=10,
        )
        response.raise_for_status()
        events = response.json()
        if isinstance(events, list) and events:
            for event in events:
                event["data"] = normalize_agenda_date(event.get("data", ""))
                event["status"] = str(event.get("status", "")).strip()
            return events
    except Exception as error:
        st.warning(
            "Não foi possível carregar a agenda diretamente do servidor. Verifique o URL do Apps Script e recarregue."
        )
        st.write(f"Erro de carregamento: {error}")

    return [dict(item) for item in DEFAULT_AGENDA]


def save_event_status(URL, event_id):
    try:
        payload = {
            "tipo_registro": "agenda_status",
            "id": event_id,
            "status": "Finalizado",
        }
        requests.post(URL, json=payload, timeout=5)
    except Exception:
        pass


def render(URL):
    st.title("📅 Agenda")

    if st.button("⟳ Recarregar agenda", key="agenda_refresh"):
        st.session_state.pop("agenda_events", None)

    agenda_events = load_agenda_events(URL)
    selected_date = st.date_input("Data", value=datetime.now(), key="agenda_data")
    selected_key = selected_date.strftime("%Y-%m-%d")

    st.caption(f"Eventos carregados: {len(agenda_events)}")

    filtered_events = [event for event in agenda_events if event.get("data", "") == selected_key]

    if filtered_events:
        st.markdown(f"### 📌 Eventos em {selected_date.strftime('%d/%m/%Y')}")
        for event in filtered_events:
            cols = st.columns([3, 1, 5, 2])
            status_text = event.get("status", "Aberto")
            status_color = "green" if status_text.lower() == "finalizado" else "orange"
            cols[0].markdown(f"**{event['evento']}**")
            cols[1].markdown(
                f"<span style='color: {status_color}; font-weight: 600'>{status_text}</span>",
                unsafe_allow_html=True,
            )
            cols[2].write(event.get("observacao", ""))

            normalized_status = normalize_status(status_text)
            if normalized_status != "finalizado":
                if cols[3].button("Finalizar", key=f"agenda_finish_{event['id']}"):
                    for stored in agenda_events:
                        if stored["id"] == event["id"]:
                            stored["status"] = "Finalizado"
                            save_event_status(URL, event["id"])
                            st.success(f"Evento '{stored['evento']}' marcado como finalizado.")
            else:
                cols[3].markdown("✅ Finalizado")
    else:
        st.info("Sem atividades")

    st.divider()
    st.subheader("📋 Agenda do dia")

    if filtered_events:
        for event in filtered_events:
            st.write(f"**{event['evento']}** — {event.get('status', 'Aberto')}")
            st.write(event.get("observacao", ""))
            st.markdown("---")
    else:
        st.write("Sem atividades")

    texto = f"""AGENDA

📆 {selected_date.strftime('%d/%m/%Y')}

{', '.join([event['evento'] for event in filtered_events]) or 'Sem atividades'}
"""

    st.text_area("Prévia", texto, height=200, key="agenda_preview")

    if st.button("📤 Compartilhar Agenda", key="agenda_share"):
        link = f"https://api.whatsapp.com/send?text={urllib.parse.quote(texto)}"
        st.markdown(f"[👉 WhatsApp]({link})")
