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
    .card {
        background-color: white; padding: 20px; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    </style>
    <div class="main-header">🏢 Vistoria Master Pro</div>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "identificacao"
if 'dados_vistoria' not in st.session_state: st.session_state.dados_vistoria = {}

# --- ETAPA 1: IDENTIFICAÇÃO (Resumo do anterior) ---
if st.session_state.etapa == "identificacao":
    st.subheader("📍 1. Dados da Unidade")
    tipo_res = st.selectbox("Tipo do Imóvel", ["Casa Térrea", "Sobrado", "Apartamento"])
    end = st.text_input("Endereço Completo")
    inspetor = st.text_input("Nome do Vistoriador")
    
    if st.button("Confirmar e Seguir ➡️"):
        if end and inspetor:
            st.session_state.dados_vistoria['info_geral'] = {
                "tipo": tipo_res, "endereco": end, "inspetor": inspetor
            }
            st.session_state.etapa = "composicao"
            st.rerun()

# --- ETAPA 2: COMPOSIÇÃO DO IMÓVEL (O QUE VOCÊ PEDIU AGORA) ---
elif st.session_state.etapa == "composicao":
    st.subheader("🏠 2. Composição do Imóvel")
    
    with st.container():
        st.write("### Selecione os Ambientes")
        
        # Itens padrão já marcados (True)
        col1, col2 = st.columns(2)
        tem_sala = col1.checkbox("Sala", value=True)
        tem_cozinha = col1.checkbox("Cozinha", value=True)
        tem_banheiro_soc = col2.checkbox("Banheiro Social", value=True)
        tem_lavanderia = col2.checkbox("Lavanderia", value=True)
        
        # Outros opcionais comuns
        tem_sacada = col1.checkbox("Sacada / Varanda")
        tem_vaga = col2.checkbox("Vaga de Garagem")

        st.write("---")
        st.write("### Dormitórios e Suítes")
        c1, c2 = st.columns(2)
        qtd_dorm = c1.number_input("Quantos Dormitórios (Simples)?", min_value=0, max_value=10, value=1)
        qtd_suit = c2.number_input("Quantas Suítes (Com Banheiro)?", min_value=0, max_value=10, value=0)

        if st.button("Iniciar Vistoria Detalhada 📝"):
            # Gerando a lista final de cômodos para a próxima etapa
            lista_final = []
            if tem_sala: lista_final.append("Sala")
            if tem_cozinha: lista_final.append("Cozinha")
            if tem_banheiro_soc: lista_final.append("Banheiro Social")
            if tem_lavanderia: lista_final.append("Lavanderia")
            if tem_sacada: lista_final.append("Sacada / Varanda")
            if tem_vaga: lista_final.append("Vaga de Garagem")
            
            # Adicionando os dormitórios dinamicamente
            for i in range(qtd_dorm):
                lista_final.append(f"Dormitório {i+1}")
            for i in range(qtd_suit):
                lista_final.append(f"Suíte {i+1}")
                lista_final.append(f"Banheiro Suíte {i+1}")
            
            st.session_state.dados_vistoria['comodos'] = lista_final
            st.session_state.etapa = "inspecao_sala" # Indo para o detalhamento da sala
            st.rerun()

    if st.sidebar.button("⬅️ Alterar Identificação"):
        st.session_state.etapa = "identificacao"
        st.rerun()

# --- ETAPA 3: ESPAÇO PARA O DETALHAMENTO DA SALA ---
elif st.session_state.etapa == "inspecao_sala":
    st.success(f"Configuração Salva: {len(st.session_state.dados_vistoria['comodos'])} ambientes no total.")
    st.info("Próximo passo: **Detalhamento da Sala**")
    
    # É AQUI que vou inserir o código da sala que você vai me explicar agora.
    st.write("---")
    if st.button("⬅️ Voltar para Composição"):
        st.session_state.etapa = "composicao"
        st.rerun()
