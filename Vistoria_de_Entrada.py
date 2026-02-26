import streamlit as st

# Configuração da página
st.set_page_config(page_title="Vistoria Técnica Pro", page_icon="🏠", layout="centered")

# --- ESTILIZAÇÃO (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #2e7d32; color: white; }
    div[data-testid="stExpander"] { border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DO FORMULÁRIO ---
def formulario_base(id_chave, nome_exibicao, eh_sacada=False):
    titulo = f"📍 {nome_exibicao.upper()}" if not eh_sacada else f"🌅 SACADA DO(A) {nome_exibicao.upper()}"
    
    with st.expander(titulo, expanded=True):
        opcoes = ["Bom estado", "Novo", "Usado"]
        opcoes_ilum = ["Bom estado", "Novo", "Usado", "Sem teste"]
        materiais_esquadrias = ["Alumínio Branco", "Alumínio Preto", "Alumínio Natural", "Madeira", "Ferro", "PVC"]
        
        # --- PISO ---
        st.markdown("**1. Piso**")
        c1, c2, c3 = st.columns(3)
        p_mat = c1.text_input("Material", value="Cerâmico", key=f"p_mat_i_{id_chave}")
        p_cor = c2.text_input("Cor do Piso", key=f"p_cor_i_{id_chave}")
        p_est = c3.selectbox("Estado", opcoes, key=f"p_est_s_{id_chave}")
        p_obs = st.text_input("Obs. do Piso", key=f"p_obs_i_{id_chave}")

        # --- PAREDES E TETO ---
        st.markdown("---")
        st.markdown("**2. Paredes e Teto**")
        c4, c5 = st.columns(2)
        with c4:
            par_cor = st.text_input("Cor Paredes", value="Branco", key=f"par_cor_in_{id_chave}")
            par_est = st.selectbox("Estado Paredes", opcoes, key=f"par_est_in_{id_chave}")
        with c5:
            tet_cor = st.text_input("Cor Teto", value="Branco", key=f"tet_cor_in_{id_chave}")
            tet_est = st.selectbox("Estado Teto", opcoes, key=f"tet_est_in_{id_chave}")

        # --- PORTAS ---
        st.markdown("---")
        st.markdown("**3. Porta e Batente**")
        cp1, cp2, cp3 = st.columns(3)
        por_mat = cp1.selectbox("Material Porta", ["Madeira", "Alumínio", "Ferro", "PVC"], key=f"p_mat_p_s_{id_chave}")
        por_cor = cp2.text_input("Cor Porta/Batente", key=f"p_cor_p_i_{id_chave}")
        por_est = cp3.selectbox("Estado Porta/Batente", opcoes, key=f"p_est_p_s_{id_chave}")
        fec_est = st.selectbox("Fechadura/Maçaneta", ["Funcionando", "Com folga", "Sem chave", "Oxidada"], key=f"fec_s_{id_chave}")

        # --- JANELAS ---
        st.markdown("---")
        st.markdown("**4. Janelas e Vidros**")
        cj1, cj2, cj3 = st.columns(3)
        jan_mat = cj1.selectbox("Material Janela", materiais_esquadrias, key=f"j_mat_s_{id_chave}")
        jan_est = cj2.selectbox("Estado Janela", opcoes, key=f"jan_est_s_{id_chave}")
        vid_est_geral = cj3.selectbox("Estado dos Vidros", opcoes, key=f"vid_est_s_{id_chave}")
        
        cj4, cj5, cj6 = st.columns(3)
        q_vidros = cj4.number_input("Qtd de Vidros", 0, 20, value=1, key=f"q_vid_{id_chave}")
        q_trincos = cj5.number_input("Qtd de Trincos", 0, 10, value=1, key=f"q_tri_{id_chave}")
        tem_avaria = cj6.radio("Possui avarias no vidro?", ["Não", "Sim"], key=f"vid_radio_{id_chave}")
        
        vid_avaria = "Íntegro"
        if tem_avaria == "Sim":
            vid_avaria = st.selectbox("Qual a avaria?", ["Trincado", "Quebrado", "Faltando"], key=f"vid_ava_sel_{id_chave}")

        # --- ELÉTRICA ---
        st.markdown("---")
        st.markdown("**5. Elétrica**")
        ce1, ce2, ce3 = st.columns(3)
        q_tom = ce1.number_input("Qtd Tomadas", 0, 50, key=f"q_tom_n_{id_chave}")
        q_int = ce2.number_input("Qtd Interruptores", 0, 50, key=f"q_int_n_{id_chave}")
        ele_est = ce3.selectbox("Estado Espelhos/Placas", opcoes, key=f"ele_est_s_{id_chave}")

        # --- ILUMINAÇÃO ---
        st.markdown("---")
        st.markdown("**6. Iluminação**")
        ilu_tipo = st.multiselect("Tipo de Iluminação", ["Lâmpada simples", "Spot LED", "Spot Plástico", "Luminária", "Dicroica", "Plafon"], default=["Lâmpada simples"], key=f"ilu_t_m_{id_chave}")
        
        possui_lampada = True
        if "Spot Plástico" in ilu_tipo:
            possui_lampada = st.checkbox("Os spots de plástico possuem lâmpadas instaladas?", value=True, key=f"check_lamp_{id_chave}")

        ci1, ci2, ci3 = st.columns(3)
        q_total = ci1.number_input("Qtd Itens Total", 0, 100, key=f"q_tot_n_{id_chave}")
        
        q_func = 0
        q_queim = 0
        if possui_lampada:
            q_func = ci2.number_input("Lâmpadas Funcionando ✅", 0, 100, key=f"q_fun_n_{id_chave}")
            q_queim = ci3.number_input("Lâmpadas Queimadas ❌", 0, 100, key=f"q_queim_n_{id_chave}")
        
        ilu_est = st.selectbox("Estado Geral Iluminação", opcoes_ilum, key=f"ilu_e_s_{id_chave}")

        # --- HIDRÁULICA / RALO ---
        res_hidro = ""
        molhados = ["cozinha", "banheiro", "serviço", "suíte", "lavabo", "lavanderia"]
        if eh_sacada or any(x in nome_exibicao.lower() for x in molhados):
            st.markdown("---")
            st.markdown("**7. Hidráulica / Ralo**")
            ch1, ch2 = st.columns(2)
            if not eh_sacada:
                met_est = ch1.selectbox("Estado Metais", opcoes, key=f"met_est_s_{id_chave}")
                lou_est = ch2.selectbox("Estado Louças", opcoes, key=f"lou_est_s_{id_chave}")
                hid_obs = st.text_input("Obs. Hidráulica", key=f"hid_obs_i_{id_chave}")
                res_hidro = f"- HIDRÁULICA: Metais em {met_est.lower()} e louças em {lou_est.lower()}. {hid_obs}\n"
            else:
                s_tem_ralo = ch1.checkbox("Possui Ralo?", key=f"s_ralo_check_{id_chave}")
                if s_tem_ralo:
                    s_ralo_mat = ch2.text_input("Material do Ralo (ex: PVC, Inox)", key=f"s_ralo_m_{id_chave}")
                    res_hidro = f"- RALO: Em {s_ralo_mat}.\n"
                else:
                    res_hidro = "- RALO: Não possui.\n"

    # --- MONTAGEM DO TEXTO ---
    tipos_ilum_str = ", ".join(ilu_tipo).lower()
    txt_ilum = f"- ILUMINAÇÃO: {q_total:02} {tipos_ilum_str} em {ilu_est.lower()}."
    
    if "spot plástico" in tipos_ilum_str and not possui_lampada:
        txt_ilum += " (Sem lâmpadas instaladas)."
    elif ilu_est.lower() != "sem teste":
        if q_queim == 0:
            txt_ilum += " Todas as lâmpadas funcionando."
        else:
            txt_ilum += f" Lâmpadas funcionando: {q_func} / Queimada(s): {q_queim}."

    cabecalho = f"### SACADA DO(A) {nome_exibicao.upper()}" if eh_sacada else f"### {nome_exibicao.upper()}"
    res = f"{cabecalho}\n"
    res += f"- PISO: {p_mat} na cor {p_cor} em {p_est.lower()}. {p_obs}\n"
    res += f"- PAREDES: Cor {par_cor}, {par_est.lower()}. TETO: Cor {tet_cor}, {tet_est.lower()}.\n"
    res += f"- PORTA: {por_mat} na cor {por_cor}, em {por_est.lower()}. Maçaneta {fec_est.lower()}.\n"
    res += f"- JANELA: {jan_mat} em {jan_est.lower()} ({q_vidros:02} vidros e {q_trincos:02} trincos). Vidros {vid_est_geral.lower()} - Estado: {vid_avaria}.\n"
    res += f"- ELÉTRICA: {q_tom} tomadas e {q_int} interruptores em {ele_est.lower()}.\n"
    res += txt_ilum + "\n"
    res += res_hidro
    
    return res + "\n"

# --- INTERFACE PRINCIPAL ---
st.title("📋 Vistoria de Entrada Profissional")

# --- CONFIGURAÇÃO DO IMÓVEL (NO CORPO DA PÁGINA) ---
with st.container():
    st.subheader("⚙️ Configuração Inicial")
    col_c1, col_c2 = st.columns(2)
    q_quartos = col_c1.number_input("Quantos Quartos (Simples)?", 0, 10, value=1)
    q_suites = col_c2.number_input("Quantas Suítes?", 0, 10, value=1)
    
    outros_comodos = st.multiselect("Selecione outros cômodos presentes:", 
                           ["Sala", "Cozinha", "Banheiro Social", "Área de Serviço", "Varanda", "Garagem"],
                           default=["Sala", "Cozinha", "Banheiro Social"])
    
    st.markdown("---")

relatorio_completo = ""

# --- PROCESSAMENTO DOS CÔMODOS ---

# SALA
if "Sala" in outros_comodos:
    tem_sacada_sala = st.checkbox("A Sala possui sacada?", key="chk_sac_sala")
    relatorio_completo += formulario_base("sala_0", "Sala")
    if tem_sacada_sala:
        relatorio_completo += formulario_base("sacada_sala", "Sala", eh_sacada=True)
    st.markdown("---")

# QUARTOS SIMPLES
for i in range(int(q_quartos)):
    nome_q = f"Quarto {i+1}"
    tem_sacada_q = st.checkbox(f"O {nome_q} possui sacada?", key=f"chk_sac_q_{i}")
    relatorio_completo += formulario_base(f"quarto_{i+1}", nome_q)
    if tem_sacada_q:
        relatorio_completo += formulario_base(f"sacada_q_{i+1}", nome_q, eh_sacada=True)
    st.markdown("---")

# SUÍTES
for i in range(int(q_suites)):
    nome_s = f"Suíte {i+1}"
    tem_sacada_s = st.checkbox(f"A {nome_s} possui sacada?", key=f"chk_sac_s_{i}")
    relatorio_completo += formulario_base(f"suite_{i+1}", nome_s)
    if tem_sacada_s:
        relatorio_completo += formulario_base(f"sacada_s_{i+1}", nome_s, eh_sacada=True)
    st.markdown("---")

# DEMAIS ÁREAS
for item in ["Cozinha", "Banheiro Social", "Área de Serviço", "Varanda", "Garagem"]:
    if item in outros_comodos and item != "Sala":
        relatorio_completo += formulario_base(item.lower().replace(" ", "_"), item)
        st.markdown("---")

# --- ÁREA FINAL ---
st.header("📄 Relatório Finalizado")
if relatorio_completo:
    st.code(relatorio_completo, language="markdown")
    st.download_button("📥 Baixar Arquivo de Vistoria", relatorio_completo, "vistoria.txt")
