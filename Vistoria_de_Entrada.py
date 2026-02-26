import streamlit as st

# Configuração da página
st.set_page_config(page_title="Gerador de Vistoria Pro", page_icon="🏠")

# --- ESTILIZAÇÃO (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- PLAYER DE MÚSICA NA LATERAL ---
with st.sidebar:
    st.title("⚙️ Menu")
    st.markdown("---")
    st.markdown("### 🎵 Rádio Imobiliária")
    # Link do YouTube (pode trocar por qualquer um)
    url_youtube = "https://www.youtube.com/watch?v=jfKfPfyJRdk" 
    st.video(url_youtube)
    st.caption("Dê o play para ouvir uma música ambiente enquanto trabalha.")

# --- FUNÇÃO DO FORMULÁRIO (VERSÃO COMPLETA) ---
def formulario_base(id_chave, nome_exibicao):
    st.markdown(f"## 🏠 {nome_exibicao}")
    opcoes = ["Bom estado", "Novo", "Usado"]
    
    # --- PISO ---
    st.markdown("**1. Piso**")
    c1, c2 = st.columns(2)
    p_mat = c1.text_input("Tipo de Piso", value="Cerâmico", key=f"p_mat_{id_chave}")
    p_est = c2.selectbox("Estado do Piso", opcoes, key=f"p_est_{id_chave}")
    p_obs = st.text_input("Obs. do Piso (riscos, peças soltas)", key=f"p_obs_{id_chave}")

    # --- PAREDES E TETO ---
    st.markdown("---")
    st.markdown("**2. Paredes e Teto**")
    c3, c4 = st.columns(2)
    with c3:
        par_cor = st.text_input("Cor das Paredes", value="Branco", key=f"par_cor_{id_chave}")
        par_est = st.selectbox("Estado das Paredes", opcoes, key=f"par_est_{id_chave}")
    with c4:
        tet_cor = st.text_input("Cor do Teto", value="Branco", key=f"tet_cor_{id_chave}")
        tet_est = st.selectbox("Estado do Teto", opcoes, key=f"tet_est_{id_chave}")
    pint_obs = st.text_input("Obs. de Pintura (furos, manchas)", key=f"pint_obs_{id_chave}")

    # --- PORTAS ---
    st.markdown("---")
    st.markdown("**3. Portas e Batentes**")
    cp1, cp2 = st.columns(2)
    por_cor = cp1.text_input("Cor da Porta/Batente", value="Branco", key=f"p_cor_{id_chave}")
    por_est = cp1.selectbox("Estado da Porta/Batente", opcoes, key=f"p_est_p_{id_chave}")
    fec_est = cp2.selectbox("Fechadura e Maçaneta", ["Funcionando", "Com folga", "Sem chave", "Oxidada"], key=f"fec_{id_chave}")
    por_obs = cp2.text_input("Obs. da Porta", key=f"p_obs_p_{id_chave}")

    # --- JANELAS ---
    st.markdown("---")
    st.markdown("**4. Janelas e Vidros**")
    cj1, cj2 = st.columns(2)
    jan_est = cj1.selectbox("Estado da Janela/Trincos", opcoes, key=f"jan_est_{id_chave}")
    vid_est = cj2.selectbox("Estado dos Vidros", ["Íntegros", "Riscados", "Trincados", "Faltando"], key=f"vid_est_{id_chave}")
    jan_obs = st.text_input("Obs. Janelas", key=f"jan_obs_{id_chave}")

    # --- ELÉTRICA ---
    st.markdown("---")
    st.markdown("**5. Elétrica (Tomadas e Interruptores)**")
    ce1, ce2 = st.columns(2)
    q_tom = ce1.number_input("Qtd Tomadas", min_value=0, step=1, key=f"q_tom_{id_chave}")
    q_int = ce2.number_input("Qtd Interruptores", min_value=0, step=1, key=f"q_int_{id_chave}")
    ele_est = st.selectbox("Estado dos Espelhos/Tomadas", opcoes, key=f"ele_est_{id_chave}")

    # --- ILUMINAÇÃO ---
    st.markdown("---")
    st.markdown("**6. Iluminação**")
    ilu_tipo = st.multiselect("Tipo de Iluminação", 
                             ["Lâmpada simples", "Spot LED", "Luminária/Plafon", "Dicroica", "Fita LED", "Apenas bocal"], 
                             default=["Lâmpada simples"], key=f"ilu_t_{id_chave}")
    ilu_est = st.selectbox("Estado da Iluminação", opcoes, key=f"ilu_e_{id_chave}")

    # --- HIDRÁULICA (Lógica para aparecer só em áreas úmidas) ---
    res_hidro = ""
    comodos_molhados = ["cozinha", "banheiro", "serviço", "lavanderia", "suíte", "lavabo"]
    if any(x in nome_exibicao.lower() for x in comodos_molhados):
        st.markdown("---")
        st.markdown("**7. Hidráulica, Metais e Louças**")
        ch1, ch2 = st.columns(2)
        met_est = ch1.selectbox("Estado Metais (Torneiras/Registros)", opcoes, key=f"met_est_{id_chave}")
        lou_est = ch2.selectbox("Estado Louças (Vaso/Pia/Tanque)", opcoes, key=f"lou_est_{id_chave}")
        hid_obs = st.text_input("Obs. Hidráulica (Vazamentos, marcas)", key=f"hid_obs_{id_chave}")
        res_hidro = f"- HIDRÁULICA: Metais em {met_est.lower()} e louças em {lou_est.lower()}. {hid_obs}\n"

    # --- MONTAGEM DO TEXTO ---
    res = f"### {nome_exibicao.upper()}\n"
    res += f"- PISO: {p_mat} em {p_est.lower()}. {p_obs}\n"
    res += f"- PAREDES: Cor {par_cor}, {par_est.lower()}. TETO: Cor {tet_cor}, {tet_est.lower()}. {pint_obs}\n"
    res += f"- PORTA: Cor {por_cor}, {por_est.lower()}. Fechadura/Maçaneta {fec_est.lower()}. {por_obs}\n"
    res += f"- JANELA: {jan_est} com vidros {vid_est.lower()}. {jan_obs}\n"
    res += f"- ELÉTRICA: {q_tom} tomadas e {q_int} interruptores em {ele_est.lower()}.\n"
    res += f"- ILUMINAÇÃO: {', '.join(ilu_tipo)} em {ilu_est.lower()}.\n"
    if res_hidro:
        res += res_hidro
    
    return res + "\n"

# --- INTERFACE PRINCIPAL ---
st.title("📝 Gerador de Vistoria de Entrada")
st.info("Preencha os campos abaixo. As seções de hidráulica aparecerão apenas nos cômodos úmidos.")

# Seleção de cômodos
comodos = st.multiselect(
    "Quais cômodos quer vistoriar?",
    ["Sala", "Cozinha", "Quarto 1", "Quarto 2", "Banheiro Social", "Suíte", "Área de Serviço", "Varanda"],
    default=["Sala", "Cozinha", "Banheiro Social"]
)

relatorio_completo = ""

# Gerar formulários dinamicamente
for item in comodos:
    id_c = item.lower().replace(" ", "_")
    texto_comodo = formulario_base(id_c, item)
    relatorio_completo += texto_comodo
    st.markdown("---")

# --- ÁREA FINAL ---
st.header("📋 Relatório Final")
if relatorio_completo:
    st.markdown(relatorio_completo)
    
    st.download_button(
        label="📥 Baixar Vistoria em .txt",
        data=relatorio_completo,
        file_name="vistoria_entrada.txt",
        mime="text/plain"
    )
else:
    st.warning("Selecione ao menos um cômodo para gerar o relatório.")
