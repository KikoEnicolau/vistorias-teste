import streamlit as st

# --- 1. CONFIGURAÇÕES INICIAIS E ESTILO ---
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

# --- 2. INICIALIZAÇÃO DO ESTADO (Prevenir o erro AttributeError) ---
if 'etapa' not in st.session_state: 
    st.session_state.etapa = "identificacao"
if 'dados_vistoria' not in st.session_state: 
    st.session_state.dados_vistoria = {}

# --- 3. DEFINIÇÃO DE OPÇÕES PADRÃO ---
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
            st.session_state.dados_vistoria['info_geral'] = {
                "tipo": tipo_res, "endereco": end, "inspetor": inspetor
            }
            st.session_state.etapa = "composicao"
            st.rerun()
        else:
            st.error("Preencha o endereço e o nome para continuar.")

# --- ETAPA 2: COMPOSIÇÃO DO IMÓVEL ---
elif st.session_state.etapa == "composicao":
    st.subheader("🏠 2. Composição do Imóvel")
    
    with st.container():
        st.write("### Cômodos Padrão")
        c1, c2 = st.columns(2)
        tem_sala = c1.checkbox("Sala", value=True)
        tem_cozinha = c1.checkbox("Cozinha", value=True)
        tem_banheiro_soc = c2.checkbox("Banheiro Social", value=True)
        tem_lavanderia = c2.checkbox("Lavanderia", value=True)

        st.write("---")
        st.write("### Dormitórios e Suítes")
        col_q, col_s = st.columns(2)
        qtd_dorm = col_q.number_input("Dormitórios (Simples)", 0, 10, 1)
        qtd_suit = col_s.number_input("Suítes", 0, 10, 0)

        if st.button("Configurar Detalhes da Sala ➡️"):
            st.session_state.etapa = "detalhe_sala" 
            st.rerun()

# --- ETAPA 3: DETALHAMENTO DA SALA (PISO E RODAPÉ) ---
elif st.session_state.etapa == "detalhe_sala":
    st.subheader("🛋️ Detalhamento: Sala")
    
    # --- SEÇÃO PISO ---
    st.markdown("#### 🏗️ Piso")
    col1, col2, col3 = st.columns(3)
    tipo_p = col1.selectbox("Tipo de Piso", OPCOES_PISO, key="s_p_t")
    est_p = col2.selectbox("Estado", OPCOES_ESTADO, key="s_p_e")
    av_p = col3.selectbox("Avarias", OPCOES_AVARIAS, key="s_p_a")
    
    # Lógica de escrita do Piso
    avaria_txt = f" com {av_p}" if av_p != "Não" else ""
    frase_piso = f"- Piso {tipo_p} {est_p}{avaria_txt}"
    st.info(f"**Escrita:** {frase_piso}")

    st.write("---")

    # --- SEÇÃO RODAPÉ ---
    st.markdown("#### 📐 Rodapé")
    tem_r = st.radio("Contém Rodapé?", ["sim", "não"], horizontal=True, key="s_r_c")
    
    frase_rodape = ""
    if tem_r == "sim":
        r1, r2, r3 = st.columns(3)
        tipo_r = r1.selectbox("Tipo de Rodapé", OPCOES_PISO, key="s_r_t")
        est_r = r2.selectbox("Estado", OPCOES_ESTADO, key="s_r_e")
        av_r = r3.selectbox("Avarias", OPCOES_AVARIAS, key="s_r_a")
        
        avaria_r_txt = f" com {av_r}" if av_r != "Não" else ""
        frase_rodape = f"- Rodapé {tipo_r} {est_r}{avaria_r_txt}"
        st.info(f"**Escrita:** {frase_rodape}")

    st.write("---")
    
    if st.button("Salvar e Próximo Item ➡️"):
        st.session_state.dados_vistoria['sala_piso'] = frase_piso
        st.session_state.dados_vistoria['sala_rodape'] = frase_rodape
        st.success("Piso e Rodapé salvos!")

    if st.sidebar.button("⬅️ Voltar"):
        st.session_state.etapa = "composicao"
        st.rerun()
