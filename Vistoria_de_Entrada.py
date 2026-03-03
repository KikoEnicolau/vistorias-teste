import streamlit as st

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-header {
        background-color: #0f172a; padding: 20px; color: white;
        text-align: center; font-size: 1.8rem; font-weight: bold;
        border-radius: 0 0 15px 15px; margin-bottom: 30px;
    }
    .status-card {
        background-color: #ffffff; padding: 15px; border-radius: 10px;
        border: 1px solid #e2e8f0; margin-bottom: 20px;
    }
    </style>
    <div class="main-header">🏢 Vistoria Master Pro</div>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "identificacao"
if 'dados_vistoria' not in st.session_state: st.session_state.dados_vistoria = {}

# --- ETAPA 1: IDENTIFICAÇÃO ---
if st.session_state.etapa == "identificacao":
    st.subheader("📍 1. Identificação da Unidade")
    
    with st.container():
        # Nova caixa de seleção conforme solicitado
        tipo_imovel = st.selectbox(
            "Tipo do Imóvel", 
            [
                "Apartamento", 
                "Casa Térrea", 
                "Sobrado", 
                "Sala Comercial", 
                "Salão", 
                "Galpão"
            ],
            key="tipo_imovel_select"
        )
        
        end = st.text_input("Endereço Completo", placeholder="Rua, número, complemento, bairro e cidade")
        
        c1, c2 = st.columns(2)
        data_v = c1.date_input("Data da Vistoria")
        finalidade = c2.selectbox("Finalidade", ["Entrada", "Saída", "Conferência"])
        
        inspetor = st.text_input("Nome do Vistoriador / Empresa")

        if st.button("Confirmar e Seguir ➡️"):
            if end and inspetor:
                # Salvando no banco de dados temporário
                st.session_state.dados_vistoria['info_geral'] = {
                    "tipo_imovel": tipo_imovel,
                    "endereco": end,
                    "data": str(data_v),
                    "finalidade": finalidade,
                    "inspetor": inspetor
                }
                # Aqui vamos mudar para a próxima etapa (Composição)
                st.session_state.etapa = "composicao"
                st.rerun()
            else:
                st.error("Por favor, preencha o endereço e o nome do vistoriador.")

# --- MANTENDO O FLUXO ---
elif st.session_state.etapa == "composicao":
    st.success(f"Imóvel identificado como: **{st.session_state.dados_vistoria['info_geral']['tipo_imovel']}**")
    st.write(f"📍 {st.session_state.dados_vistoria['info_geral']['endereco']}")
    
    st.write("---")
    st.write("### Próximo passo: Definir os ambientes (cômodos)")
    
    if st.button("⬅️ Alterar Dados Iniciais"):
        st.session_state.etapa = "identificacao"
        st.rerun()
