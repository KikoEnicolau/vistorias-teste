import streamlit as st

# --- ESTILO VISUAL ---
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

# --- INICIALIZAÇÃO DO ESTADO ---
if 'etapa' not in st.session_state: 
    st.session_state.etapa = "identificacao"
if 'dados_vistoria' not in st.session_state: 
    st.session_state.dados_vistoria = {}

# --- ETAPA 1: IDENTIFICAÇÃO ---
if st.session_state.etapa == "identificacao":
    st.subheader("📍 1. Dados da Unidade")
    
    with st.container():
        # Seleção restrita conforme solicitado
        tipo_residencia = st.selectbox(
            "Tipo do Imóvel", 
            ["Casa Térrea", "Sobrado", "Apartamento"],
            key="tipo_res_select"
        )
        
        end = st.text_input("Endereço Completo", placeholder="Rua, número, complemento, bairro...")
        
        c1, c2 = st.columns(2)
        data_v = c1.date_input("Data da Vistoria")
        finalidade = c2.selectbox("Finalidade", ["Entrada", "Saída", "Conferência"])
        
        inspetor = st.text_input("Nome do Vistoriador")

        if st.button("Confirmar e Definir Cômodos ➡️"):
            if end and inspetor:
                st.session_state.dados_vistoria['info_geral'] = {
                    "tipo_imovel": tipo_residencia,
                    "endereco": end,
                    "data": str(data_v),
                    "finalidade": finalidade,
                    "inspetor": inspetor
                }
                st.session_state.etapa = "composicao"
                st.rerun()
            else:
                st.error("Preencha o endereço e o nome para continuar.")

# --- ETAPA 2: TRANSIÇÃO ---
elif st.session_state.etapa == "composicao":
    st.success(f"Imóvel: **{st.session_state.dados_vistoria['info_geral']['tipo_imovel']}**")
    st.info(f"📍 {st.session_state.dados_vistoria['info_geral']['endereco']}")
    
    st.write("---")
    st.subheader("🏠 2. Composição do Imóvel")
    st.write("Quais ambientes vamos vistoriar hoje?")
    
    # Aqui vamos inserir a lista de cômodos no próximo passo
    
    if st.sidebar.button("⬅️ Alterar Identificação"):
        st.session_state.etapa = "identificacao"
        st.rerun()
