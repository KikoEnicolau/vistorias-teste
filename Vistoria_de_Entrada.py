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
def formulario_base(id_chave, nome_exibicao):
    with st.expander(f"📍 {nome_exibicao.upper()}", expanded=True):
        opcoes = ["Bom estado", "Novo", "Usado"]
        materiais = ["Alumínio", "Madreia", "Ferro", "PVC", "Vidro Temperado"]
        
        # --- PISO ---
        st.markdown("**1. Piso**")
        c1, c2, c3 = st.columns(3)
        p_mat = c1.text_input("Material", value="Cerâmico", key=f"p_mat_{id_chave}")
        p_cor = c2.text_input("Cor do Piso", key=f"p_cor_{id_chave}")
        p_est = c3.selectbox("Estado", opcoes, key=f"p_est_{id_chave}")
        p_obs = st.text_input("Obs. do Piso", key=f"p_obs_{id_chave}")

        # --- PAREDES E TETO ---
        st.markdown("---")
        st.markdown("**2. Paredes e Teto**")
        c4, c5 = st.columns(2)
        with c4:
            par_cor = st.text_input("Cor Paredes", value="Branco", key=f"par_cor_{id_chave}")
            par_est = st.selectbox("Estado Paredes", opcoes, key=f"par_est_{id_chave}")
        with c5:
            tet_cor = st.text_input("Cor Teto", value="Branco", key=f"tet_cor_{id_chave}")
            tet_est = st.selectbox("Estado Teto", opcoes, key=f"tet_est_{id_chave}")

        # --- PORTAS ---
        st.markdown("---")
        st.markdown("**3. Porta e Batente**")
        cp1, cp2, cp3 = st.columns(3)
        por_mat = cp1.selectbox("Material Porta", materiais, index=1, key=f"p_mat_p_{id_chave}")
        por_cor = cp2.text_input("Cor Porta/Batente", key=f"p_cor_{id_chave}")
        por_est = cp3.selectbox("Estado Porta", opcoes, key=f"p_est_p_{id_chave}")
        fec_est = st.selectbox("Fechadura/Maçaneta", ["Funcionando", "Com folga", "Sem chave", "Oxidada"], key=f"fec_{id_chave}")

        # --- JANELAS ---
        st.markdown("---")
        st.markdown("**4. Janelas**")
        cj1, cj2, cj3 = st.columns(3)
        jan_mat = cj1.selectbox("Material Janela", materiais, key=f"j_mat_{id_chave}")
        jan_est = cj2.selectbox("Estado Janela", opcoes, key=f"jan_est_{id_chave}")
        vid_est = cj3.selectbox("Estado Vidros", ["Íntegros", "Riscados", "Trincados"], key=f"vid_est_{id_chave}")

        # --- ELÉTRICA ---
        st.markdown("---")
        st.markdown("**5. Elétrica**")
        ce1, ce2, ce3 = st.columns(3)
        q_tom = ce1.number_input("Qtd Tomadas", 0, 50, key=f"q_tom_{id_chave}")
        q_int = ce2.number_input("Qtd Interruptores", 0, 50, key=f"q_int_{id_chave}")
        ele_est = ce3.selectbox("Estado Espelhos", opcoes, key=f"ele_est_{id_chave}")

        # --- ILUMINAÇÃO ---
        st.markdown("---")
        st.markdown("**6. Iluminação**")
        ilu_tipo = st.multiselect("Tipo", ["Lâmpada simples", "Spot LED", "Spot Plástico", "Luminária", "Dicroica"], default=["Lâmpada simples"], key=f"ilu_t_{id_chave}")
        
        c_i1, c_i2, c_i3 = st.columns(3)
        q_total = c_i1.number_input("Qtd Total Lâmpadas/Spots", 0, 100, key=f"q_tot_{id_chave}")
        q_func = c_i2.number_input("Funcionando ✅", 0, 100, key=f"q_fun_{id_chave}")
        q_queim = c_i3.number_input("Queimadas ❌", 0, 100, key=f"q_queim_{id_chave}")
        ilu_est = st.selectbox("Estado Geral Iluminação", opcoes, key=f"ilu_e_{id_chave}")

        # --- HIDRÁULICA ---
        res_hidro = ""
        molhados = ["cozinha", "banheiro", "serviço", "suíte", "lavabo"]
        if any(x in nome_exibicao.lower() for x in molhados):
            st.markdown("---")
            st.markdown("**7. Hidráulica**")
            ch1, ch2 = st.columns(2)
            met_est = ch1.selectbox("Estado Metais", opcoes, key=f"met_est_{id_chave}")
            lou_est = ch2.selectbox("Estado Louças", opcoes, key=f"lou_est_{id_chave}")
            hid_obs = st.text_input("Obs. Hidráulica", key=f"hid_obs_{id_chave}")
            res_hidro = f"- HIDRÁULICA: Metais em {met_est.lower()} e louças em {lou_est.lower()}. {hid_obs}\n"

    # --- MONTAGEM DO TEXTO ---
    res = f"### {nome_exibicao.upper()}\n"
    res += f"- PISO: {p_mat} na cor {p_cor} em {p_est.lower()}. {p_obs}\n"
    res += f"- PAREDES: Cor {par_cor}, {par_est.lower()}. TETO: Cor {tet_cor}, {tet_est.lower()}.\n"
    res += f"- PORTA: {por_mat} na cor {por_cor}, em {por_est.lower()}. Maçaneta {fec_est.lower()}.\n"
    res += f"- JANELA: {jan_mat} em {jan_est.lower()} com vidros {vid_est.lower()}.\n"
    res += f"- ELÉTRICA: {q_tom} tomadas e {q_int} interruptores em {ele_est.lower()}.\n"
    res += f"- ILUMINAÇÃO: {', '.join(ilu_tipo)} ({q_total} unidades). Funcionando: {q_func} / Queimadas: {q_queim}. Geral: {ilu_est.lower()}.\n"
    if res_hidro: res += res_hidro
    
    return res + "\n"

# --- INTERFACE PRINCIPAL ---
st.title("📋 Vistoria de Entrada Detalhada")

with st.container():
    st.subheader("⚙️ Configuração do Imóvel")
    c_config1, c_config2 = st.columns(2)
    qtd_quartos = c_config1.number_input("Quantos Quartos (Simples)?", 0, 10, value=1)
    qtd_suites = c_config2.number_input("Quantas Suítes?", 0, 10, value=1)
    
    outros = st.multiselect("Outros Cômodos:", 
                           ["Sala", "Cozinha", "Banheiro Social", "Área de Serviço", "Varanda", "Garagem"],
                           default=["Sala", "Cozinha", "Banheiro Social"])

# Lista final de cômodos
lista_comodos = []
if "Sala" in outros: lista_comodos.append("Sala")
for i in range(qtd_quartos): lista_comodos.append(f"Quarto {i+1}")
for i in range(qtd_suites): lista_comodos.append(f"Suíte {i+1}")
if "Cozinha" in outros: lista_comodos.append("Cozinha")
if "Banheiro Social" in outros: lista_comodos.append("Banheiro Social")
if "Área de Serviço" in outros: lista_comodos.append("Área de Serviço")
if "Varanda" in outros: lista_comodos.append("Varanda")
if "Garagem" in outros: lista_comodos.append("Garagem")

relatorio_completo = ""

# Gerar formulários
for item in lista_comodos:
    id_c = item.lower().replace(" ", "_")
    relatorio_completo += formulario_base(id_c, item)

# --- ÁREA DE DOWNLOAD ---
st.markdown("---")
st.header("📄 Relatório Finalizado")
if relatorio_completo:
    st.code(relatorio_completo, language="markdown")
    st.download_button("📥 Baixar Arquivo de Vistoria", relatorio_completo, "vistoria.txt")
