import streamlit as st
from datetime import datetime

# --- CONFIGURAÇÕES E ESTADO ---
st.set_page_config(page_title="Vistoria Master Pro", page_icon="🏢", layout="wide")

if 'etapa' not in st.session_state: st.session_state.etapa = "identificacao"
if 'dados_vistoria' not in st.session_state: st.session_state.dados_vistoria = {}
if 'comodos_lista' not in st.session_state: st.session_state.comodos_lista = []
if 'historico_vistorias' not in st.session_state: st.session_state.historico_vistorias = []

# OPÇÕES GERAIS
OPCOES_PISO = ["porcelanato", "de cerâmica", "vinílico", "laminado", "de madeira", "frio"]
OPCOES_ESTADO = ["em bom estado", "novo", "usado"]
OPCOES_AVARIAS = ["Não", "riscos", "manchas", "trincado"]
OPCOES_AV_PAREDE = ["Não", "furos de prego", "manchas", "descascada", "mofo", "riscos"]
CORES_TINTA = ["Branco", "Gelo", "Palha", "Cinza Platina", "Areia"]

# --- CABEÇALHO ---
st.markdown('<div style="background-color:#0f172a;padding:20px;color:white;text-align:center;font-size:1.8rem;font-weight:bold;border-radius:0 0 15px 15px;margin-bottom:30px;">🏢 Vistoria Master Pro</div>', unsafe_allow_html=True)

# --- NAVEGAÇÃO LATERAL ---
with st.sidebar:
    if st.button("🚫 RECOMEÇAR TUDO"):
        st.session_state.etapa = "identificacao"; st.session_state.dados_vistoria = {}; st.rerun()

# --- ETAPA 1 E 2 (IDENTIFICAÇÃO E COMPOSIÇÃO) ---
if st.session_state.etapa == "identificacao":
    st.subheader("📍 1. Dados da Unidade")
    tipo_res = st.selectbox("Tipo", ["Casa Térrea", "Sobrado", "Apartamento"])
    end = st.text_input("Endereço Completo")
    insp = st.text_input("Vistoriador")
    if st.button("Seguir ➡️"):
        if end and insp:
            st.session_state.dados_vistoria['info_geral'] = {"tipo": tipo_res, "endereco": end, "inspetor": insp, "data": datetime.now().strftime("%d/%m/%Y")}
            st.session_state.etapa = "composicao"; st.rerun()

elif st.session_state.etapa == "composicao":
    st.subheader("🏠 2. Composição")
    c1, c2 = st.columns(2)
    t_sala = c1.checkbox("Sala", value=True); t_coz = c1.checkbox("Cozinha", value=True)
    t_ban = c2.checkbox("Banheiro Social", value=True); t_lav = c2.checkbox("Lavanderia", value=True)
    q_dorm = st.number_input("Dormitórios", 0, 10, 1); q_suit = st.number_input("Suítes", 0, 10, 0)
    if st.button("Ir para Detalhamento ➡️"):
        lista = []
        if t_sala: lista.append("Sala")
        if t_coz: lista.append("Cozinha")
        if t_ban: lista.append("Banheiro Social")
        if t_lav: lista.append("Lavanderia")
        for i in range(q_dorm): lista.append(f"Dormitório {i+1}")
        for i in range(q_suit): lista.append(f"Suíte {i+1}"); lista.append(f"Banheiro {i+1}")
        st.session_state.comodos_lista = lista; st.session_state.etapa = "detalhamento"; st.rerun()

# --- ETAPA 3: DETALHAMENTO ---
elif st.session_state.etapa == "detalhamento":
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
                frase_p = f"- Piso {tp} {ep}{av_txt}"; st.info(frase_p); texto_relatorio += frase_p + "\n"

            # --- RODAPÉ ---
            with st.expander("📐 Rodapé", expanded=False):
                if st.radio("Contém Rodapé?", ["sim", "não"], horizontal=True, key=f"r_c_{key_id}") == "sim":
                    c1, c2, c3 = st.columns(3)
                    tr = c1.selectbox("Tipo", OPCOES_PISO, key=f"r_t_{key_id}")
                    er = c2.selectbox("Estado", OPCOES_ESTADO, key=f"r_e_{key_id}")
                    ar = c3.selectbox("Avarias", OPCOES_AVARIAS, key=f"r_a_{key_id}")
                    av_r_txt = f" com {ar}" if ar != "Não" else ""
                    frase_r = f"- Rodapé em piso {tr} {er}{av_r_txt}"; st.info(frase_r); texto_relatorio += frase_r + "\n"

            # --- PAREDES (Lógica Solicitada) ---
            with st.expander("🧱 Paredes", expanded=False):
                tipo_pa = st.selectbox("Tipo de Parede", ["Alvenaria", "Azulejos"], key=f"pa_t_{key_id}")
                av_pa = st.selectbox("Avarias", OPCOES_AV_PAREDE, key=f"pa_a_{key_id}")
                av_pa_txt = f" com {av_pa}" if av_pa != "Não" else ""
                
                if tipo_pa == "Azulejos":
                    est_az = st.selectbox("Estado", ["nova", "usada"], key=f"pa_e_az_{key_id}")
                    frase_pa = f"- Paredes com azulejos ate o teto {est_az}{av_pa_txt}"
                else:
                    c1, c2 = st.columns(2)
                    cor_pa = c1.selectbox("Cor da Tinta", CORES_TINTA, key=f"pa_cor_{key_id}")
                    est_pintura = c2.selectbox("Estado da Pintura", ["nova", "usada"], key=f"pa_e_al_{key_id}")
                    frase_pa = f"- Paredes em alvenaria em bom estado, na cor {cor_pa.lower()} com pintura {est_pintura}{av_pa_txt}"
                
                st.info(frase_pa); texto_relatorio += frase_pa + "\n"

            # --- TETO ---
            with st.expander("☁️ Teto", expanded=False):
                c1, c2, c3 = st.columns(3)
                tt = c1.selectbox("Tipo de Teto", ["gesso liso", "forro PVC", "laje rebocada"], key=f"t_t_{key_id}")
                et = c2.selectbox("Estado", OPCOES_ESTADO, key=f"t_e_{key_id}")
                at = c3.selectbox("Avarias", OPCOES_AV_PAREDE, key=f"t_a_{key_id}")
                av_t_txt = f" com {at}" if at != "Não" else ""
                frase_t = f"- Teto em {tt} {et}{av_t_txt}"; st.info(frase_t); texto_relatorio += frase_t + "\n"
            
            texto_relatorio += "\n"

    st.divider()
    st.download_button("📥 BAIXAR RELATÓRIO (.txt)", texto_relatorio, file_name=f"Vistoria_{st.session_state.dados_vistoria['info_geral']['data']}.txt")
