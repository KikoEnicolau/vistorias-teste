import streamlit as st

# --- 1. CONFIGURAÇÕES INICIAIS ---
st.set_page_config(page_title="Vistoria Master Pro", page_icon="🏢", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-header {
        background-color: #0f172a; padding: 20px; color: white;
        text-align: center; font-size: 1.8rem; font-weight: bold;
        border-radius: 0 0 15px 15px; margin-bottom: 30px;
    }
    /* Estilo para os Expanders (setinhas) */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: 1px solid #e2e8f0 !important;
    }
    </style>
    <div class="main-header">🏢 Vistoria Master Pro</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DO ESTADO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "identificacao"
if 'dados_vistoria' not in st.session_state: st.session_state.dados_vistoria = {}
if 'comodos_lista' not in st.session_state: st.session_state.comodos_lista = []

OPCOES_PISO = ["porcelanato", "de cerâmica", "vinílico", "laminado", "de madeira", "frio"]
OPCOES_ESTADO = ["em bom estado", "novo", "usado"]
OPCOES_AVARIAS = ["Não", "riscos", "manchas", "trincado"]

# --- ETAPA 1: IDENTIFICAÇÃO ---
if st.session_state.etapa == "identificacao":
    st.subheader("📍 1. Dados da Unidade")
    tipo_res = st.selectbox("Tipo do Imóvel", ["Casa Térrea", "Sobrado", "Apartamento"])
    end = st.text_input("Endereço Completo")
    inspetor = st.text_input("Nome do Vistoriador")
    
    if st.button("Confirmar e Seguir ➡️"):
        if end and inspetor:
            st.session_state.dados_vistoria['info_geral'] = {"tipo": tipo_res, "endereco": end, "inspetor": inspetor}
            st.session_state.etapa = "composicao"
            st.rerun()

# --- ETAPA 2: COMPOSIÇÃO ---
elif st.session_state.etapa == "composicao":
    st.subheader("🏠 2. Composição do Imóvel")
    c1, c2 = st.columns(2)
    t_sala = c1.checkbox("Sala", value=True)
    t_coz = c1.checkbox("Cozinha", value=True)
    t_ban = c2.checkbox("Banheiro Social", value=True)
    t_lav = c2.checkbox("Lavanderia", value=True)
    
    col_q, col_s = st.columns(2)
    q_dorm = col_q.number_input("Dormitórios (Simples)", 0, 10, 1)
    q_suit = col_s.number_input("Suítes", 0, 10, 0)

    if st.button("Ir para Detalhamento ➡️"):
        lista = []
        if t_sala: lista.append("Sala")
        if t_coz: lista.append("Cozinha")
        if t_ban: lista.append("Banheiro Social")
        if t_lav: lista.append("Lavanderia")
        for i in range(q_dorm): lista.append(f"Dormitório {i+1}")
        for i in range(q_suit):
            lista.append(f"Suíte {i+1}"); lista.append(f"Banheiro Suíte {i+1}")
        st.session_state.comodos_lista = lista
        st.session_state.etapa = "detalhamento"
        st.rerun()

# --- ETAPA 3: DETALHAMENTO COM EXPANDERS (SETINHAS) ---
elif st.session_state.etapa == "detalhamento":
    st.info(f"📍 {st.session_state.dados_vistoria['info_geral']['endereco']}")
    
    abas = st.tabs(st.session_state.comodos_lista)

    for i, nome_comodo in enumerate(st.session_state.comodos_lista):
        with abas[i]:
            key_id = f"{nome_comodo}_{i}"
            
            # --- EXPANDER PISO ---
            with st.expander("🏗️ Inspeção de Piso", expanded=False):
                c1, c2, c3 = st.columns(3)
                tipo_p = c1.selectbox("Tipo de Piso", OPCOES_PISO, key=f"p_t_{key_id}")
                est_p = c2.selectbox("Estado", OPCOES_ESTADO, key=f"p_e_{key_id}")
                av_p = c3.selectbox("Avarias", OPCOES_AVARIAS, key=f"p_a_{key_id}")
                
                av_txt = f" com {av_p}" if av_p != "Não" else ""
                frase_piso = f"- Piso {tipo_p} {est_p}{av_txt}"
                st.info(f"Escrita: {frase_piso}")

            # --- EXPANDER RODAPÉ ---
            with st.expander("📐 Inspeção de Rodapé", expanded=False):
                tem_r = st.radio("Contém Rodapé?", ["sim", "não"], horizontal=True, key=f"r_c_{key_id}")
                if tem_r == "sim":
                    r1, r2, r3 = st.columns(3)
                    tipo_r = r1.selectbox("Tipo de Rodapé", OPCOES_PISO, key=f"r_t_{key_id}")
                    est_r = r2.selectbox("Estado", OPCOES_ESTADO, key=f"r_e_{key_id}")
                    av_r = r3.selectbox("Avarias", OPCOES_AVARIAS, key=f"r_a_{key_id}")
                    
                    av_r_txt = f" com {av_r}" if av_r != "Não" else ""
                    frase_rodape = f"- Rodapé em piso {tipo_r} {est_r}{av_r_txt}"
                    st.info(f"Escrita: {frase_rodape}")
                else:
                    st.write("Item não existente neste cômodo.")

    if st.sidebar.button("⬅️ Reiniciar"):
        st.session_state.etapa = "composicao"; st.rerun()
