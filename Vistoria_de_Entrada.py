import streamlit as st
from datetime import datetime

# --- 1. CONFIGURAÇÕES E ESTILO ---
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

# OPÇÕES PADRONIZADAS
OPCOES_PISO = ["porcelanato", "de cerâmica", "vinílico", "laminado", "de madeira", "frio"]
OPCOES_ESTADO = ["em bom estado", "novo", "usado"]
OPCOES_AVARIAS = ["Não", "riscos", "manchas", "trincado", "furos", "mofo"]
CORES_TINTA = ["Branco", "Gelo", "Palha", "Cinza Platina", "Areia"]

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
    
    texto_relatorio = f"LAUDO DE VISTORIA\nEndereço: {st.session_state.dados_vistoria['info_geral']['endereco']}\n\n"
    
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
                tipo_pa = st.selectbox("Tipo de Parede", ["Alvenaria", "Azulejos"], key=f"pa_t_{key_id}")
                av_pa = st.selectbox("Avarias", OPCOES_AVARIAS, key=f"pa_a_{key_id}")
                av_pa_txt = f" com {av_pa}" if av_pa != "Não" else ""
                
                if tipo_pa == "Azulejos":
                    est_az = st.selectbox("Estado do Azulejo", ["nova", "usada"], key=f"pa_e_az_{key_id}")
                    frase_pa = f"- Paredes com azulejos ate o teto {est_az}{av_pa_txt}"
                else:
                    c1, c2 = st.columns(2)
                    cor_pa = c1.selectbox("Cor da Tinta", CORES_TINTA, key=f"pa_cor_{key_id}")
                    est_pintura = c2.selectbox("Estado da Pintura", ["nova", "usada"], key=f"pa_e_al_{key_id}")
                    frase_pa = f"- Paredes em alvenaria em bom estado, na cor {cor_pa.lower()} com pintura {est_pintura}{av_pa_txt}"
                st.info(frase_pa)
                texto_relatorio += frase_pa + "\n"

            # --- TETO ---
            with st.expander("☁️ Teto", expanded=False):
                c1, c2, c3 = st.columns(3)
                cor_t = c1.selectbox("Cor do Teto", CORES_TINTA, key=f"t_cor_{key_id}")
                est_t = c2.selectbox("Estado da Pintura", ["nova", "usada"], key=f"t_est_{key_id}")
                av_t = c3.selectbox("Avarias", OPCOES_AVARIAS, key=f"t_av_{key_id}")
                
                tem_gesso = st.radio("Acabamento em gesso?", ["não", "sim"], horizontal=True, key=f"t_gesso_{key_id}")
                av_t_txt = f" com {av_t}" if av_t != "Não" else ""
                frase_teto = f"- Teto na cor {cor_t.lower()}, com pintura {est_t}{av_t_txt}"
                
                if tem_gesso == "sim":
                    est_g = st.selectbox("Estado do Gesso", ["nova", "usada"], key=f"t_g_est_{key_id}")
                    frase_teto += f", com acabamento em gesso {est_g}"
                
                st.info(frase_teto)
                texto_relatorio += frase_teto + "\n"
            
            texto_relatorio += "\n"

    st.divider()
    st.download_button("📥 BAIXAR VISTORIA (.txt)", texto_relatorio, file_name=f"Vistoria_{datetime.now().strftime('%Y%m%d')}.txt")

    if st.sidebar.button("⬅️ Reiniciar"):
        st.session_state.etapa = "identificacao"; st.rerun()
