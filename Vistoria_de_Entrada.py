import streamlit as st
from datetime import datetime

# --- CONFIGURAÇÕES ---
st.set_page_config(page_title="Vistoria Master Pro", page_icon="🏢", layout="wide")

if 'etapa' not in st.session_state: st.session_state.etapa = "identificacao"
if 'dados_vistoria' not in st.session_state: st.session_state.dados_vistoria = {}
if 'comodos_lista' not in st.session_state: st.session_state.comodos_lista = []

# OPÇÕES PADRONIZADAS
OPCOES_ESTADO = ["nova", "usada"]
OPCOES_AVARIAS = ["Não", "riscos", "manchas", "furos", "mofo", "trincas"]
CORES_TINTA = ["Branco", "Gelo", "Palha", "Cinza Platina", "Areia"]

# --- ETAPAS INICIAIS (RESUMIDAS PARA O FLUXO) ---
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

# --- ETAPA 3: DETALHAMENTO (FOCO NO TETO AGORA) ---
elif st.session_state.etapa == "detalhamento":
    st.info(f"📍 {st.session_state.dados_vistoria['info_geral']['endereco']}")
    texto_relatorio = f"LAUDO DE VISTORIA\n\n"
    abas = st.tabs(st.session_state.comodos_lista)

    for i, nome_comodo in enumerate(st.session_state.comodos_lista):
        with abas[i]:
            key_id = f"{nome_comodo}_{i}"
            texto_relatorio += f"[{nome_comodo.upper()}]\n"
            
            # --- PISO E RODAPÉ E PAREDE (OCULTOS AQUI PARA FOCO NO TETO) ---
            # ... (Lógica anterior mantida internamente) ...

            # --- TETO (Sua nova solicitação) ---
            with st.expander("☁️ Inspeção de Teto", expanded=False):
                c1, c2, c3 = st.columns(3)
                cor_teto = c1.selectbox("Cor do Teto", CORES_TINTA, key=f"t_cor_{key_id}")
                est_teto = c2.selectbox("Estado da Pintura", OPCOES_ESTADO, key=f"t_est_{key_id}")
                av_teto = c3.selectbox("Avarias no Teto", OPCOES_AVARIAS, key=f"t_av_{key_id}")
                
                tem_gesso = st.radio("Acabamento em gesso?", ["não", "sim"], horizontal=True, key=f"t_gesso_check_{key_id}")
                
                # Base da frase
                av_txt = f" com {av_teto}" if av_teto != "Não" else ""
                frase_teto = f"- Teto na cor {cor_teto.lower()}, com pintura {est_teto}{av_txt}"
                
                # Adiciona gesso se selecionado
                if tem_gesso == "sim":
                    est_gesso = st.selectbox("Estado do Gesso", OPCOES_ESTADO, key=f"t_gesso_est_{key_id}")
                    frase_teto += f", com acabamento em gesso {est_gesso}"
                
                st.info(frase_teto)
                texto_relatorio += frase_teto + "\n\n"

    st.divider()
    st.download_button("📥 BAIXAR RELATÓRIO (.txt)", texto_relatorio, file_name="vistoria.txt")
