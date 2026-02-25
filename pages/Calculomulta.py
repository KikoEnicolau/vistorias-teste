import streamlit as st
from datetime import date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Cálculo de Multa por Datas", layout="wide")

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
st.title("🧮 Calculadora de Multa Rescisória")
st.write("Cálculo baseado em meses comerciais de 30 dias.")

# Início do formulário
with st.form("calculo_datas"):
    
    # 1. PERÍODO DE DESOCUPAÇÃO (AGORA EM CIMA)
    st.subheader("📅 1. Período de Desocupação")
    col_d1, col_d2 = st.columns(2)
    
    # format="DD/MM/YYYY" coloca o calendário no padrão brasileiro
    data_saida = col_d1.date_input("Data da entrega das chaves", value=date.today(), format="DD/MM/YYYY")
    data_fim_contrato = col_d2.date_input("Data do fim do contrato", value=date.today(), format="DD/MM/YYYY")
    
    st.markdown("---")
    
    # 2. VALORES E CONTRATO (AGORA EMBAIXO)
    st.subheader("💰 2. Valores do Contrato")
    valor_aluguel = st.number_input("Valor do Aluguel Mensal (R$)", min_value=0.0, step=100.0, value=1500.0)
    
    c1, c2 = st.columns(2)
    meses_contrato_total = c1.number_input("Duração total do contrato (Meses)", min_value=1, value=30)
    multa_pactuada = c2.number_input("Multa em contrato (Qtd. Aluguéis)", min_value=1, value=3)
    
    calcular = st.form_submit_button("Calcular Multa Proporcional")

if calcular:
    if data_saida >= data_fim_contrato:
        st.success("✅ A data de saída é posterior ou igual ao fim do contrato. Não há multa a pagar!")
    else:
        # Lógica de cálculo (Meses comerciais de 30 dias)
        anos = data_fim_contrato.year - data_saida.year
        meses = data_fim_contrato.month - data_saida.month
        dias = data_fim_contrato.day - data_saida.day
        
        total_meses_restantes = (anos * 12) + meses
        dias_restantes_comerciais = (total_meses_restantes * 30) + dias
        
        dias_totais_contrato = meses_contrato_total * 30
        multa_cheia = valor_aluguel * multa_pactuada
        
        # Valor Proporcional
        valor_multa = (multa_cheia / dias_totais_contrato) * dias_restantes_comerciais

        st.divider()
        st.subheader("📊 Resultado da Rescisão")
        
        res1, res2 = st.columns(2)
        res1.metric("Dias faltantes", f"{dias_restantes_comerciais} dias")
        res2.metric("Valor da Multa", f"R$ {valor_multa:,.2f}")
        
        # Formatação das datas para o texto final
        data_saida_br = data_saida.strftime('%d/%m/%Y')
        data_fim_br = data_fim_contrato.strftime('%d/%m/%Y')

        # Texto pronto para enviar
        texto_whatsapp = (
            f"Prezado cliente,\n\n"
            f"Conforme solicitado, segue o cálculo da multa rescisória proporcional:\n\n"
            f"📍 Entrega das chaves: {data_saida_br}\n"
            f"📍 Final do contrato: {data_fim_br}\n"
            f"⏳ Dias proporcionais restantes: {dias_restantes_comerciais} dias\n"
            f"💵 Valor total da multa: *R$ {valor_multa:,.2f}*\n\n"
            f"Cálculo realizado considerando meses de 30 dias."
        )
        st.text_area("Cópia para WhatsApp/E-mail:", texto_whatsapp, height=200)
