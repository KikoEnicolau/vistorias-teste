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
st.title("🧮 Calculadora de Multa (Por Período)")
st.write("Cálculo automático de dias faltantes baseado em meses de 30 dias.")

with st.form("calculo_datas"):
    valor_aluguel = st.number_input("Valor do Aluguel (R$)", min_value=0.0, step=100.0, value=1500.0)
    
    c1, c2 = st.columns(2)
    meses_contrato_total = c1.number_input("Duração total do contrato (Meses)", min_value=1, value=30)
    multa_pactuada = c2.number_input("Multa rescisória (Qtd. Aluguéis)", min_value=1, value=3)

    st.markdown("---")
    st.subheader("📅 Período de Desocupação")
    
    col_d1, col_d2 = st.columns(2)
    data_saida = col_d1.date_input("Data da entrega das chaves (Saída)", date.today())
    data_fim_contrato = col_d2.date_input("Data do fim do contrato (Findar)", date.today())
    
    calcular = st.form_submit_button("Calcular Multa Proporcional")

if calcular:
    if data_saida >= data_fim_contrato:
        st.success("✅ A data de saída é posterior ou igual ao fim do contrato. Não há multa!")
    else:
        # Lógica para cálculo considerando todos os meses como 30 dias
        # 1. Calculamos a diferença total em dias calendários primeiro
        diff = data_fim_contrato - data_saida
        
        # 2. Ajustamos para a regra de meses comerciais (30 dias)
        # Calculamos quantos meses inteiros e dias sobram
        anos = data_fim_contrato.year - data_saida.year
        meses = data_fim_contrato.month - data_saida.month
        dias = data_fim_contrato.day - data_saida.day
        
        total_meses_restantes = (anos * 12) + meses
        
        # Ajuste dos dias para a regra de 30 dias
        dias_restantes_comerciais = (total_meses_restantes * 30) + dias
        
        # Valores Totais
        dias_totais_contrato = meses_contrato_total * 30
        multa_cheia = valor_aluguel * multa_pactuada
        
        # Valor Final
        valor_multa = (multa_cheia / dias_totais_contrato) * dias_restantes_comerciais

        st.divider()
        st.subheader("📊 Resultado")
        
        res1, res2 = st.columns(2)
        res1.metric("Dias faltantes", f"{dias_restantes_comerciais} dias")
        res2.metric("Valor da Multa", f"R$ {valor_multa:,.2f}")
        
        st.info(f"O cálculo considerou que faltam **{dias_restantes_comerciais} dias** para o fim do contrato (base 30 dias/mês).")

        # Texto para WhatsApp
        texto_whatsapp = (
            f"Prezado cliente,\n\n"
            f"Conforme vistoria e entrega das chaves em {data_saida.strftime('%d/%m/%Y')}:\n"
            f"- Data final do contrato: {data_fim_contrato.strftime('%d/%m/%Y')}\n"
            f"- Dias proporcionais faltantes: {dias_restantes_comerciais} dias\n"
            f"- Valor da multa rescisória: *R$ {valor_multa:,.2f}*\n\n"
            f"Cálculo baseado em meses comerciais (30 dias)."
        )
        st.text_area("Cópia para WhatsApp:", texto_whatsapp, height=180)
