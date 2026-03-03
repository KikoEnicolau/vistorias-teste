import streamlit as st
from docx import Document
from docx.shared import Inches
import io

# 1. CONFIGURAÇÃO VISUAL
st.set_page_config(page_title="Vistoria Master Pro", page_icon="🏢", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-header {
        background-color: #0f172a; padding: 20px; color: white;
        text-align: center; font-size: 1.8rem; font-weight: bold;
        border-radius: 0 0 15px 15px; margin-bottom: 30px;
    }
    </style>
    <div class="main-header">🏢 Vistoria Master Pro</div>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE MEMÓRIA (Session State)
if 'etapa' not in st.session_state: st.session_state.etapa = "identificacao"
if 'dados_vistoria' not in st.session_state: st.session_state.dados_vistoria = {}
if 'fotos' not in st.session_state: st.session_state.fotos = {}

# 3. ETAPA: IDENTIFICAÇÃO DO IMÓVEL
if st.session_state.etapa == "identificacao":
    st.subheader("📍 Dados Iniciais")
    with st.container():
        end = st.text_input("Endereço do Imóvel", placeholder="Ex: Rua das Palmeiras, 123 - Apto 42")
        c1, c2 = st.columns(2)
        data = c1.date_input("Data da Vistoria")
        tipo = c2.selectbox("Tipo de Vistoria", ["Entrada", "Saída", "Conferência"])
        inspetor = st.text_input("Nome do Vistoriador")
        
        if st.button("Configurar Primeiro Cômodo ➡️"):
            if end and inspetor:
                st.session_state.dados_vistoria['info_geral'] = {
                    "endereco": end, "data": str(data), "tipo": tipo, "inspetor": inspetor
                }
                st.session_state.etapa = "inspecao"
                st.rerun()
            else:
                st.warning("Preencha o endereço e o nome do vistoriador para continuar.")

# 4. ETAPA: INSPEÇÃO (Onde entraremos com os cômodos)
elif st.session_state.etapa == "inspecao":
    st.info(f"Imóvel: {st.session_state.dados_vistoria['info_geral']['endereco']}")
    
    # É AQUI que vamos inserir os cômodos um por um!
    st.write("---")
    st.write("### 🚧 Módulo de Cômodo em Construção...")
    
    if st.button("⬅️ Voltar"):
        st.session_state.etapa = "identificacao"
        st.rerun()
