import streamlit as st
from datetime import datetime
import urllib.parse


def moeda(v):
    return f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_valor(v):
    if v > 0:
        return f"+R$ {moeda(v)}"
    elif v < 0:
        return f"-R$ {moeda(v)}"
    else:
        return f"R$ {moeda(v)}"


def campo_valor(label, key):
    v = st.number_input(label, value=0.0, key=key)
    if v < 0:
        st.markdown("<span style='color:red'>🔴 Valor negativo</span>", unsafe_allow_html=True)
    return v


def render():
    st.title("🧾 Gestão Diária")

    loja = st.text_input("🚟 Loja", "10 - São Lourenço", key="gestao_loja")
    data = st.date_input("📆 Data", value=datetime.now(), key="gestao_data")
    hora = st.text_input("⏰ Horário", datetime.now().strftime("%H:%M"), key="gestao_hora")

    nomes = [
        "Filipe Ambrozio - Assistente Prevenção",
        "Luiz Cláudio - GS Prevenção",
        "Fiscal",
    ]
    responsavel = st.selectbox("👤 Responsável", nomes, key="gestao_responsavel")

    st.divider()

    st.subheader("📌 Vendas")
    venda = campo_valor("Venda Acumulada", "gestao_venda")
    ating = st.number_input("Atingimento (%)", value=0.0, key="gestao_ating")

    estoque = campo_valor("Estoque Geral", "gestao_estoque")

    st.subheader("⚠️ Quebras")
    pi = campo_valor("Quebra PI", "gestao_pi")
    pni = campo_valor("Quebra PNI", "gestao_pni")
    total = campo_valor("Quebra Total", "gestao_total")

    st.subheader("💰 Financeiro")
    contratos = campo_valor("Contratos", "gestao_contratos")
    acordos = campo_valor("Acordos", "gestao_acordos")
    receitas = campo_valor("Receitas", "gestao_receitas")
    reversao = campo_valor("Reversão", "gestao_reversao")

    st.subheader("📊 Resultado")
    qfinal = campo_valor("Quebra Final", "gestao_qfinal")
    qmeta = st.number_input("Quebra Meta (%)", value=0.0, key="gestao_qmeta")
    qreal = st.number_input("Quebra Real (%)", value=0.0, key="gestao_qreal")

    troca = campo_valor("Estoque Troca", "gestao_troca")
    t30 = campo_valor("Estoque T +30", "gestao_t30")

    texto = f"""🧾 GESTÃO DIÁRIA

🚟 Loja: {loja}
📆 Data: {data.strftime('%d/%m/%Y')}
⏰ Horário: {hora}h

👤 Responsável: {responsavel}

📌 Venda Acumulada Mês:
R$ {moeda(venda)}
Atingimento da meta de venda {ating:.0f}%

Estoque Geral Loja R$ {moeda(estoque)}

Quebra PI: {formatar_valor(pi)}
Quebra PNI: {formatar_valor(pni)}
Quebra Total: {formatar_valor(total)}

Contratos: {formatar_valor(contratos)}
Acordos: {formatar_valor(acordos)}
Receitas: {formatar_valor(receitas)}
Reversão: {formatar_valor(reversao)}

Quebra Final: {formatar_valor(qfinal)}
Quebra Meta: {qmeta:.2f}%
Quebra Real: {qreal:.2f}%

Estoque Troca: R$ {moeda(troca)}
Estoque T +30: R$ {moeda(t30)}
"""

    st.text_area("📋 Pré-visualização", texto, height=400, key="gestao_preview")

    if st.button("📤 Compartilhar Gestão", key="gestao_share"):
        link = f"https://api.whatsapp.com/send?text={urllib.parse.quote(texto)}"
        st.success("Clique abaixo para enviar")
        st.markdown(f"[👉 Abrir WhatsApp]({link})")
