import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Cálculo de Multa por Dias", layout="wide")

# --- LINKS DAS IMAGENS ---
logo_url = "https://i.postimg.cc/9Myjqr69/Captura-de-tela-2026-02-24-160708.png" 
foto_esquerda = "https://i.postimg.cc/ZnJXBjF5/image.png" 
foto_direita = "https://i.postimg.cc/ZnJXBjF5/image.png"

# --- ESTILIZAÇÃO CSS ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background: 
            url("{foto_esquerda}") left center / 25% no-repeat fixed,
            url("{foto_direita}") right center / 25% no-repeat fixed,
            #f0f2f6;
    }}
    .block-container {{
        background-color: rgba(255, 255, 255, 0.98);
        padding: 40px !important;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        max-width: 800px;
        margin: auto;
    }}
    h1, h2, h3, p, span, label {{ color: #000000 !important; }}
    </style>
    """,
    unsafe_allow_html=True
)

st.image(logo_url, width=220)
st.title("🧮 Cálculo de Multa Rescisória (Por Dias)")
st.write("Cálculo proporcional exato considerando todos os meses com 30 dias.")

with st.form("calculo_multa_dias"):
    valor_aluguel = st.number_input("Valor do Aluguel (R$)", min_value=0.0, step=100.0, value=1500.0)
    
    col1, col2 = st.columns(2)
    meses_contrato = col1.number_input("Duração do Contrato (Meses)", min_value=1, value=30)
    multa_pactuada = col2.number_input("Multa (Qtd. Aluguéis)", min_value=1, value=3)
    
    st.markdown("---")
    st.write("**Tempo Cumprido:**")
    c3, c4 = st.columns(2)
    meses_pagos = c3.number_input("Meses inteiros pagos", min_value=0, value=12)
    dias_extras = c4.number_input("Dias extras do mês atual", min_value=0, max_value=30, value=0)
    
    calcular = st.form_submit_button("Calcular Multa Exata")

if calcular:
    # Lógica baseada em meses de 30 dias
    total_dias_contrato = meses_contrato * 30
    dias_cumpridos = (meses_pagos * 30) + dias_extras
    dias_restantes = total_dias_contrato - dias_cumpridos
    
    if dias_restantes <= 0:
        st.success("✅ O contrato já foi cumprido integralmente ou ultrapassado. Sem multa!")
    else:
        multa_total_cheia = valor_aluguel * multa_pactuada
        # Cálculo: (Multa / Total de Dias) * Dias Restantes
        valor_multa_proporcional = (multa_total_cheia / total_dias_contrato) * dias_restantes
        
        st.divider()
        st.subheader("📊 Resultado Detalhado")
        
        m1, m2 = st.columns(2)
        m1.metric("Dias Restantes", f"{dias_restantes} dias")
        m2.metric("Valor da Multa", f"R$ {valor_multa_proporcional:,.2f}")
        
        # Detalhamento para o cliente
        texto_detalhado = (
            f"O contrato possui {total_dias_contrato} dias totais ({meses_contrato} meses).\n"
            f"Foram cumpridos {dias_cumpridos} dias.\n"
            f"A multa é calculada sobre os {dias_restantes} dias que faltam."
        )
        st.info(texto_detalhado)

        # Texto para WhatsApp
        texto_whatsapp = (
            f"Prezado cliente,\n\n"
            f"Segue o cálculo da multa rescisória proporcional:\n"
            f"- Aluguel: R$ {valor_aluguel:,.2f}\n"
            f"- Prazo faltante: {dias_restantes} dias\n"
            f"- Valor a pagar: *R$ {valor_multa_proporcional:,.2f}*\n\n"
            f"Cálculo baseado na Lei 8.245/91."
        )
        st.text_area("Cópia para WhatsApp:", texto_whatsapp, height=150)
