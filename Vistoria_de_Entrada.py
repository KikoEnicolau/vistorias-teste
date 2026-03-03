import streamlit as st
from datetime import datetime

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
    .stDownloadButton button { width: 100%; background-color: #16a34a !important; color: white !important; }
    .streamlit-expanderHeader { background-color: white !important; font-weight: bold !important; border: 1px solid #e2e8f0 !important; }
    </style>
    <div class="main-header">🏢 Vistoria Master Pro</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DO ESTADO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "identificacao"
if 'dados_vistoria' not in st.session_state: st.session_state.dados_vistoria = {}
if 'comodos_lista' not in st.session_state: st.session_state.comodos_lista = []
if 'historico_vistorias' not in st.session_state: st.session_state.historico_vistorias = []

# --- 3. OPÇÕES DE SELEÇÃO ---
OPCOES_PISO = ["porcelanato", "de cerâmica", "vinílico", "laminado", "de madeira", "frio"]
OPCOES_ESTADO = ["em bom estado", "novo", "usado"]
OPCOES_AVARIAS = ["Não", "riscos", "manchas", "trincado"]

OPCOES_PAREDE = ["pintura látex", "pintura acrílica", "azulejo", "papel de parede", "reboco"]
OPCOES_AV_PAREDE = ["Não", "furos de prego", "manchas", "descascada", "mofo", "riscos"]

OPCOES_TETO = ["gesso liso", "forro PVC", "laje rebocada", "gesso com moldura"]

# --- 4. BARRA LATERAL ---
with st.sidebar:
    st.subheader("💾 Histórico Recente")
    if st.session_state.historico_vistorias:
        for hist in st.session_state.historico_vistorias[-2:]:
            st.caption(f"📅 {hist['data']} - {hist['endereco'][:20]}...")
    st.write("---")
    if st.button("🚫 RECOMEÇAR TUDO"):
        st.session_state.etapa = "identificacao"
        st.session_state.dados_vistoria = {}
        st.rerun()

# --- ETAPA 1: IDENTIFICAÇÃO ---
if st.session_state.etapa == "identificacao":
    st.subheader("📍 1. Dados da Unidade")
    tipo_res = st.selectbox("Tipo do Imóvel", ["Casa Térrea", "Sobrado", "Apartamento"])
    end = st.text_input("Endereço Completo")
    insp = st.text_input("Nome do Vistoriador")
    
    if st.button("Confirmar e Seguir ➡️"):
        if end and insp:
            st.session_state.dados_vistoria['info_geral'] = {
                "tipo": tipo_res, "endereco": end, "inspetor": insp, "data": datetime.now().strftime("%d/%m/%Y")
            }
            st.session_state.etapa = "composicao"
            st.rerun()

# --- ETAPA 2: COMPOSIÇÃO ---
elif st.session_state.etapa == "composicao":
    st.subheader("🏠 2. Composição do Imóvel")
    c1, c2 = st.columns(2)
    t_sala = c1.checkbox("Sala", value=True); t_coz = c1.checkbox("Cozinha", value=True)
    t_ban = c2.checkbox("Banheiro Social", value=True); t_lav = c2.checkbox("Lavanderia", value=True)
    
    st.write("---")
    q_dorm = st.number_input("Dormitórios (Simples)", 0, 10, 1)
    q_suit = st.number_input("Suítes", 0, 10, 0)

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

# --- ETAPA 3: DETALHAMENTO ---
elif st.session_state.etapa == "detalhamento":
    st.info(f"📍 {st.session_state.dados_vistoria['info_geral']['endereco']}")
    
    texto_relatorio = f"LAUDO DE VISTORIA - {st.session_state.dados_vistoria['info_geral']['tipo'].upper()}\n"
    texto_relatorio += f"Endereço: {st.session_state.dados_vistoria['info_geral']['endereco']}\n\n"
    
    abas = st.tabs(st.session_state.comodos_lista)

    for i, nome_comodo in enumerate(st.session_state.comodos_lista):
        with abas[i]:
            key_id = f"{nome_comodo}_{i}"
            texto_relatorio += f"[{nome_comodo.upper()}]\n"
            
            # --- PISO ---
            with st.expander("🏗️ Piso", expanded=False):
                c1, c2, c3 = st.columns(3)
                tp = c1.selectbox("Tipo de Piso", OPCOES_PISO, key=f"p_t_{key_id}")
                ep = c2.selectbox("Estado", OPCOES_ESTADO, key=f"p_e_{key_id}")
                ap = c3.selectbox("Avarias", OPCOES_AVARIAS, key=f"p_a_{key_id}")
                av_txt = f" com {ap}" if ap != "Não" else ""
                frase_piso = f"- Piso {tp} {ep}{av_txt}"
                st.info(frase_piso)
                texto_relatorio += frase_piso + "\n"

            # --- RODAPÉ ---
            with st.expander("📐 Rodapé", expanded=False):
                tem_r = st.radio("Contém Rodapé?", ["sim", "não"], horizontal=True, key=f"r_c_{key_id}")
                if tem_r == "sim":
                    r1, r2, r3 = st.columns(3)
                    tipo_r = r1.selectbox("Tipo de Rodapé", OPCOES_PISO, key=f"r_t_{key_id}")
                    est_r = r2.selectbox("Estado", OPCOES_ESTADO, key=f"r_e_{key_id}")
                    av_r = r3.selectbox("Avarias", OPCOES_AVARIAS, key=f"r_a_{key_id}")
                    av_r_txt = f" com {av_r}" if av_r != "Não" else ""
                    frase_rodape = f"- Rodapé em piso {tipo_r} {est_r}{av_r_txt}"
                    st.info(frase_rodape)
                    texto_relatorio += frase_rodape + "\n"

            # --- PAREDES ---
            with st.expander("🧱 Paredes", expanded=False):
                c1, c2, c3 = st.columns(3)
                t_par = c1.selectbox("Tipo de Parede", OPCOES_PAREDE, key=f"par_t_{key_id}")
                e_par = c2.selectbox("Estado", OPCOES_ESTADO, key=f"par_e_{key_id}")
                a_par = c3.selectbox("Avarias", OPCOES_AV_PAREDE, key=f"par_a_{key_id}")
                av_par_txt = f" com {a_par}" if a_par != "Não" else ""
                frase_parede = f"- Paredes em {t_par} {e_par}{av_par_txt}"
                st.info(frase_parede)
                texto_relatorio += frase_parede + "\n"

            # --- TETO ---
            with st.expander("☁️ Teto", expanded=False):
                c1, c2, c3 = st.columns(3)
                t_teto = c1.selectbox("Tipo de Teto", OPCOES_TETO, key=f"tet_t_{key_id}")
                e_teto = c2.selectbox("Estado", OPCOES_ESTADO, key=f"tet_e_{key_id}")
                a_teto = c3.selectbox("Avarias", OPCOES_AV_PAREDE, key=f"tet_a_{key_id}")
                av_teto_txt = f" com {a_teto}" if a_teto != "Não" else ""
                frase_teto = f"- Teto em {t_teto} {e_teto}{av_teto_txt}"
                st.info(frase_teto)
                texto_relatorio += frase_teto + "\n"
            
            texto_relatorio += "\n"

    st.divider()
    
    col1, col2 = st.columns(2)
    if col1.button("💾 Salvar no Histórico"):
        st.session_state.historico_vistorias.append(st.session_state.dados_vistoria['info_geral'])
        st.success("Histórico atualizado!")

    col2.download_button(
        label="📥 BAIXAR VISTORIA (.txt)",
        data=texto_relatorio,
        file_name=f"Vistoria_{datetime.now().strftime('%Y%m%d')}.txt"
    )
