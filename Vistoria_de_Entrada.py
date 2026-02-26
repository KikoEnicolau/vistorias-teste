import streamlit as st

# Configuração da página
st.set_page_config(page_title="Vistoria Técnica Pro", page_icon="🏠", layout="centered")

# --- LISTAS DE OPÇÕES PARA SELEÇÃO RÁPIDA ---
OPCOES_ESTADO = ["Bom estado", "Novo", "Usado"]
OPCOES_CORES = ["Branco", "Gelo", "Cinza", "Bege", "Preto", "Marrom", "Amadeirado", "Off-white", "Outra"]
OPCOES_PISO_MAT = ["Cerâmico", "Porcelanato", "Laminado", "Vinílico", "Ardósia", "Cimento Queimado", "Taco/Madeira", "Carpete"]
OPCOES_PORTA_MAT = ["Madeira", "Alumínio Branco", "Alumínio Preto", "Ferro", "PVC", "Vidro Temperado"]
OPCOES_JANELA_MAT = ["Alumínio Branco", "Alumínio Preto", "Alumínio Natural", "Madeira", "Ferro", "PVC"]
OPCOES_RALO_MAT = ["PVC Branco", "PVC Cinza", "Inox", "Plástico Cromado", "Oculto (Próprio piso)"]

# --- ESTILIZAÇÃO (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #2e7d32; color: white; }
    div[data-testid="stExpander"] { border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px; }
    h4 { color: #2e7d32; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

def formulario_base(id_chave, nome_exibicao, eh_sacada=False):
    titulo = f"📍 {nome_exibicao.upper()}" if not eh_sacada else f"🌅 SACADA DO(A) {nome_exibicao.upper()}"
    
    with st.expander(titulo, expanded=True):
        texto_acumulado = ""

        # --- PISO ---
        incluir_piso = st.checkbox("Incluir Piso?", value=False, key=f"inc_piso_{id_chave}")
        if incluir_piso:
            st.markdown("#### 1. Piso")
            c1, c2, c3 = st.columns(3)
            p_mat = c1.selectbox("Material", OPCOES_PISO_MAT, key=f"p_mat_s_{id_chave}")
            p_cor = c2.selectbox("Cor do Piso", OPCOES_CORES, key=f"p_cor_s_{id_chave}")
            p_est = c3.selectbox("Estado", OPCOES_ESTADO, key=f"p_est_s_{id_chave}")
            p_obs = st.text_input("Obs. Curta (opcional)", key=f"p_obs_i_{id_chave}")
            texto_acumulado += f"- PISO: {p_mat} na cor {p_cor} em {p_est.lower()}. {p_obs}\n"

        # --- PAREDES E TETO ---
        incluir_par = st.checkbox("Incluir Paredes/Teto?", value=False, key=f"inc_par_{id_chave}")
        if incluir_par:
            st.markdown("---")
            st.markdown("#### 2. Paredes e Teto")
            c4, c5, c6, c7 = st.columns(4)
            par_cor = c4.selectbox("Cor Paredes", OPCOES_CORES, key=f"par_cor_s_{id_chave}")
            par_est = c5.selectbox("Estado Paredes", OPCOES_ESTADO, key=f"par_est_s_{id_chave}")
            tet_cor = c6.selectbox("Cor Teto", OPCOES_CORES, key=f"tet_cor_s_{id_chave}")
            tet_est = c7.selectbox("Estado Teto", OPCOES_ESTADO, key=f"tet_est_s_{id_chave}")
            texto_acumulado += f"- PAREDES: Cor {par_cor}, {par_est.lower()}. TETO: Cor {tet_cor}, {tet_est.lower()}.\n"

        # --- PORTAS ---
        incluir_porta = st.checkbox("Incluir Porta/Batente?", value=False, key=f"inc_porta_{id_chave}")
        if incluir_porta:
            st.markdown("---")
            st.markdown("#### 3. Porta e Batente")
            cp1, cp2, cp3, cp4 = st.columns(4)
            por_mat = cp1.selectbox("Material", OPCOES_PORTA_MAT, key=f"p_mat_p_s_{id_chave}")
            por_cor = cp2.selectbox("Cor", OPCOES_CORES, key=f"p_cor_p_s_{id_chave}")
            por_est = cp3.selectbox("Estado", OPCOES_ESTADO, key=f"p_est_p_s_{id_chave}")
            fec_est = cp4.selectbox("Maçaneta", ["Funcionando", "Com folga", "Sem chave", "Oxidada"], key=f"fec_s_{id_chave}")
            texto_acumulado += f"- PORTA: {por_mat} na cor {por_cor}, em {por_est.lower()}. Maçaneta {fec_est.lower()}.\n"

        # --- JANELAS ---
        incluir_janela = st.checkbox("Incluir Janelas?", value=False, key=f"inc_janela_{id_chave}")
        if incluir_janela:
            st.markdown("---")
            st.markdown("#### 4. Janelas e Vidros")
            cj1, cj2, cj3 = st.columns(3)
            jan_mat = cj1.selectbox("Material Janela", OPCOES_JANELA_MAT, key=f"j_mat_s_{id_chave}")
            jan_est = cj2.selectbox("Estado Janela", OPCOES_ESTADO, key=f"jan_est_s_{id_chave}")
            vid_est_geral = cj3.selectbox("Estado dos Vidros", OPCOES_ESTADO, key=f"vid_est_s_{id_chave}")
            
            cj4, cj5, cj6 = st.columns(3)
            q_vidros = cj4.number_input("Qtd Vidros", 0, 20, value=1, key=f"q_vid_{id_chave}")
            q_trincos = cj5.number_input("Qtd Trincos", 0, 10, value=1, key=f"q_tri_{id_chave}")
            tem_avaria = cj6.radio("Avarias no vidro?", ["Não", "Sim"], key=f"vid_radio_{id_chave}")
            
            vid_avaria = "Íntegro"
            if tem_avaria == "Sim":
                vid_avaria = st.selectbox("Qual avaria?", ["Trincado", "Quebrado", "Faltando"], key=f"vid_ava_sel_{id_chave}")
            texto_acumulado += f"- JANELA: {jan_mat} em {jan_est.lower()} ({q_vidros:02} vidros e {q_trincos:02} trincos). Vidros {vid_est_geral.lower()} - Estado: {vid_avaria}.\n"

        # --- ELÉTRICA ---
        incluir_eletrica = st.checkbox("Incluir Elétrica?", value=False, key=f"inc_ele_{id_chave}")
        if incluir_eletrica:
            st.markdown("---")
            st.markdown("#### 5. Elétrica")
            ce1, ce2, ce3 = st.columns(3)
            q_tom = ce1.number_input("Qtd Tomadas", 0, 50, key=f"q_tom_n_{id_chave}")
            q_int = ce2.number_input("Qtd Interruptores", 0, 50, key=f"q_int_n_{id_chave}")
            ele_est = ce3.selectbox("Estado Placas", OPCOES_ESTADO, key=f"ele_est_s_{id_chave}")
            
            txt_quadro = ""
            tem_quadro = st.checkbox("Possui Quadro de Disjuntores?", key=f"chk_quadro_{id_chave}")
            if tem_quadro:
                c_q1, c_q2 = st.columns(2)
                mat_quadro = c_q1.selectbox("Material", ["Plástico", "Ferro", "Madeira"], key=f"mat_quadro_{id_chave}")
                est_q_geral = c_q2.selectbox("Estado Quadro", OPCOES_ESTADO, key=f"est_quadro_geral_{id_chave}")
                
                if mat_quadro == "Madeira":
                    cor_q = st.selectbox("Cor Madeira", OPCOES_CORES, key=f"cor_quadro_{id_chave}")
                    txt_quadro = f" Quadro em {mat_quadro} {cor_q} ({est_q_geral.lower()})."
                else:
                    txt_quadro = f" Quadro em {mat_quadro} ({est_q_geral.lower()})."
            texto_acumulado += f"- ELÉTRICA: {q_tom} tomadas e {q_int} interruptores em {ele_est.lower()}.{txt_quadro}\n"

        # --- ILUMINAÇÃO ---
        incluir_ilum = st.checkbox("Incluir Iluminação?", value=False, key=f"inc_ilum_{id_chave}")
        if incluir_ilum:
            st.markdown("---")
            st.markdown("#### 6. Iluminação")
            ilu_tipo = st.multiselect("Tipo", ["Lâmpada simples", "Spot LED", "Spot Plástico", "Luminária", "Plafon"], default=["Lâmpada simples"], key=f"ilu_t_m_{id_chave}")
            
            possui_lampada = True
            if "Spot Plástico" in ilu_tipo:
                possui_lampada = st.checkbox("Possui lâmpadas nos spots?", value=True, key=f"check_lamp_{id_chave}")

            ci1, ci2, ci3, ci4 = st.columns(4)
            q_total = ci1.number_input("Qtd Total", 0, 100, key=f"q_tot_n_{id_chave}")
            ilu_est = ci2.selectbox("Estado", ["Bom estado", "Novo", "Usado", "Sem teste"], key=f"ilu_e_s_{id_chave}")
            
            q_func, q_queim = 0, 0
            if possui_lampada:
                q_func = ci3.number_input("Funcionando ✅", 0, 100, key=f"q_fun_n_{id_chave}")
                q_queim = ci4.number_input("Queimadas ❌", 0, 100, key=f"q_queim_n_{id_chave}")
            
            est_formatado = f"em {ilu_est.lower()}" if "bom estado" in ilu_est.lower() else ilu_est.lower()
            txt_ilum = f"- ILUMINAÇÃO: {q_total:02} {', '.join(ilu_tipo).lower()} {est_formatado}."
            if "spot plástico" in str(ilu_tipo).lower() and not possui_lampada:
                txt_ilum += " (Sem lâmpadas)."
            elif ilu_est.lower() != "sem teste":
                txt_ilum += " Todas funcionando." if q_queim == 0 else f" Ok: {q_func} / Queimada: {q_queim}."
            texto_acumulado += txt_ilum + "\n"

        # --- HIDRÁULICA / RALO ---
        if eh_sacada or any(x in nome_exibicao.lower() for x in ["cozinha", "banheiro", "serviço", "suíte"]):
            incluir_hidro = st.checkbox("Incluir Hidráulica/Ralo?", value=False, key=f"inc_hidro_{id_chave}")
            if incluir_hidro:
                st.markdown("---")
                st.markdown("#### 7. Hidráulica / Ralo")
                ch1, ch2 = st.columns(2)
                if not eh_sacada:
                    met_est = ch1.selectbox("Estado Metais", OPCOES_ESTADO, key=f"met_est_s_{id_chave}")
                    lou_est = ch2.selectbox("Estado Louças", OPCOES_ESTADO, key=f"lou_est_s_{id_chave}")
                    texto_acumulado += f"- HIDRÁULICA: Metais em {met_est.lower()} e louças em {lou_est.lower()}.\n"
                else:
                    s_tem_ralo = ch1.checkbox("Possui Ralo?", value=False, key=f"s_ralo_check_{id_chave}")
                    if s_tem_ralo:
                        s_ralo_mat = ch2.selectbox("Material do Ralo", OPCOES_RALO_MAT, key=f"s_ralo_m_s_{id_chave}")
                        texto_acumulado += f"- RALO: {s_ralo_mat}.\n"

    prefixo = f"### SACADA DO(A) {nome_exibicao.upper()}" if eh_sacada else f"### {nome_exibicao.upper()}"
    return f"{prefixo}\n{texto_acumulado}\n"

# --- INTERFACE PRINCIPAL ---
st.title("📋 Vistoria Pro: Rápida e Fácil")

with st.container():
    st.subheader("⚙️ O que vamos vistoriar hoje?")
    col1, col2 = st.columns(2)
    q_quartos = col1.number_input("Quartos Simples", 0, 10, value=1)
    q_suites = col2.number_input("Suítes", 0, 10, value=0)
    outros = st.multiselect("Outras áreas:", ["Sala", "Cozinha", "Banheiro Social", "Área de Serviço", "Garagem"], default=["Sala", "Cozinha"])

relatorio_total = ""

if "Sala" in outros:
    relatorio_total += formulario_base("sala_0", "Sala")
    if st.checkbox("A Sala tem sacada?", key="chk_sac_sala"):
        relatorio_total += formulario_base("sacada_sala", "Sala", eh_sacada=True)
    st.markdown("---")

for i in range(int(q_quartos)):
    nome = f"Quarto {i+1}"
    relatorio_total += formulario_base(f"quarto_{i+1}", nome)
    if st.checkbox(f"O {nome} tem sacada?", key=f"chk_sac_q_{i}"):
        relatorio_total += formulario_base(f"sacada_q_{i+1}", nome, eh_sacada=True)
    st.markdown("---")

for i in range(int(q_suites)):
    nome = f"Suíte {i+1}"
    relatorio_total += formulario_base(f"suite_{i+1}", nome)
    if st.checkbox(f"A {nome} tem sacada?", key=f"chk_sac_s_{i}"):
        relatorio_total += formulario_base(f"sacada_s_{i+1}", nome, eh_sacada=True)
    st.markdown("---")

for item in outros:
    if item != "Sala":
        relatorio_total += formulario_base(item.lower().replace(" ", "_"), item)
        st.markdown("---")

st.header("📄 Relatório Pronto")
if relatorio_total:
    st.code(relatorio_total, language="markdown")
    st.download_button("📥 Baixar Vistoria (.txt)", relatorio_total, "vistoria.txt")
