import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Vistoria de Entrada", layout="wide")

# --- LINKS DAS IMAGENS ---
logo_url = "https://i.postimg.cc/9Myjqr69/Captura-de-tela-2026-02-24-160708.png" 
foto_esquerda = "https://i.postimg.cc/ZnJXBjF5/image.png" 
foto_direita = "https://i.postimg.cc/XvnbywK0/image.png"

# --- ESTILIZAÇÃO CSS (LATERAIS) ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background: 
            url("{foto_esquerda}") left center / 25% no-repeat fixed,
            url("{foto_direita}") right center / 25% no-repeat fixed,
            #f0f2f6; 
    }}
    .block-container {{
        background-color: rgba(255, 255, 255, 0.98);
        padding: 40px !important;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        max-width: 850px; 
        margin: auto;
        border: 1px solid #ddd;
    }}
    @media (max-width: 768px) {{
        .stApp {{ background: #ffffff; }}
        .block-container {{ max-width: 95%; padding: 15px !important; }}
    }}
    h1, h2, h3, p, span, label, .stMarkdown {{ color: #000000 !important; }}
    </style>
    """,
    unsafe_allow_html=True
)

st.image(logo_url, width=220)
st.title("📋 Vistoria de Entrada") # Nome alterado aqui

st.markdown("---") # Divisória inicial (Botão removido conforme solicitado)

# --- 1. CONFIGURAÇÃO DO IMÓVEL ---
st.header("1. Configuração do Imóvel")
col_dorm, col_suit = st.columns(2)
num_dormitorios = col_dorm.number_input("Quantos Dormitórios (Simples)?", min_value=0, value=1, step=1)
num_suites = col_suit.number_input("Quantas Suítes?", min_value=0, value=0, step=1)

# --- FUNÇÃO AUXILIAR PARA CÔMODOS COMPLETOS ---
def formulario_base(id_chave, nome_exibicao):
    st.markdown(f"### 🏠 {nome_exibicao}")
    
    opcoes = ["Bom estado", "Novo", "Usado"]
    
    # --- PISO ---
    st.markdown("**1. Piso**")
    c1, c2 = st.columns(2)
    p_mat = c1.text_input("Tipo de Piso", value="Cerâmico", key=f"p_mat_{id_chave}")
    p_est = c2.selectbox("Estado do Piso", opcoes, key=f"p_est_{id_chave}")
    p_obs = st.text_input("Obs. do Piso", placeholder="Ex: Riscos leves, peça trincada...", key=f"p_obs_{id_chave}")

    # --- PAREDES E TETO ---
    st.markdown("---")
    st.markdown("**2. Paredes e Teto**")
    c3, c4 = st.columns(2)
    par_est = c3.selectbox("Estado das Paredes", opcoes, key=f"par_est_{id_chave}")
    tet_est = c4.selectbox("Estado do Teto", opcoes, key=f"tet_est_{id_chave}")
    pint_obs = st.text_input("Obs. de Pintura/Estrutura", placeholder="Ex: Furos de prego, manchas...", key=f"pint_obs_{id_chave}")

    # --- PORTAS E JANELAS ---
    st.markdown("---")
    st.markdown("**3. Portas, Janelas e Vidros**")
    c5, c6 = st.columns(2)
    por_est = c5.selectbox("Estado da Porta/Maçaneta", opcoes, key=f"por_est_{id_chave}")
    jan_est = c6.selectbox("Estado da Janela/Vidros", opcoes, key=f"jan_est_{id_chave}")
    esq_obs = st.text_input("Obs. de Esquadrias", placeholder="Ex: Vidro riscado, tranca dura...", key=f"esq_obs_{id_chave}")

    # --- ELÉTRICA ---
    st.markdown("---")
    st.markdown("**4. Elétrica e Iluminação**")
    c7, c8 = st.columns(2)
    ele_est = c7.selectbox("Estado de Tomadas/Interruptores", opcoes, key=f"ele_est_{id_chave}")
    ilu_est = c8.selectbox("Estado da Iluminação/Bocais", opcoes, key=f"ilu_est_{id_chave}")
    ele_obs = st.text_input("Obs. Elétrica", placeholder="Ex: Campainha não funciona, tampa solta...", key=f"ele_obs_{id_chave}")

    # --- HIDRÁULICA E METAIS (Para Banheiros/Cozinha) ---
    st.markdown("---")
    st.markdown("**5. Hidráulica, Metais e Louças**")
    c9, c10 = st.columns(2)
    met_est = c9.selectbox("Estado de Torneiras/Registros", opcoes, key=f"met_est_{id_chave}")
    lou_est = c10.selectbox("Estado de Vasos/Pias/Tanques", opcoes, key=f"lou_est_{id_chave}")
    hid_obs = st.text_input("Obs. Hidráulica", placeholder="Ex: Vazamento leve, ralo entupido...", key=f"hid_obs_{id_chave}")

    # --- TEXTO FINAL DO RELATÓRIO ---
    res = f"**{nome_exibicao.upper()}**\n"
    res += f"- PISO: {p_mat} em {p_est.lower()}. {p_obs}\n"
    res += f"- PAREDES/TETO: Paredes em {par_est.lower()} e teto em {tet_est.lower()}. {pint_obs}\n"
    res += f"- PORTAS/JANELAS: Portas em {por_est.lower()} e janelas em {jan_est.lower()}. {esq_obs}\n"
    res += f"- ELÉTRICA: Tomadas em {ele_est.lower()} e iluminação em {ilu_est.lower()}. {ele_obs}\n"
    res += f"- HIDRÁULICA: Metais em {met_est.lower()} e louças em {lou_est.lower()}. {hid_obs}\n"
    
    return res + "\n"

def criar_secao_comodo(id_chave, nome_exibicao, tem_sacada=True, eh_suite=False):
    with st.expander(f"📍 {nome_exibicao.upper()}"):
        incluir = st.checkbox(f"Incluir {nome_exibicao}", key=f"inc_{id_chave}")
        texto_acumulado = ""
        if incluir:
            texto_acumulado += formulario_base(id_chave, nome_exibicao)
            if eh_suite:
                st.markdown("#### 🚿 Banheiro da Suíte")
                texto_acumulado += formulario_base(f"banh_{id_chave}", f"Banheiro {nome_exibicao}")
            if tem_sacada:
                st.markdown("#### 🌅 Sacada")
                add_sacada = st.checkbox(f"Adicionar Sacada em {nome_exibicao}?", key=f"check_sac_{id_chave}")
                if add_sacada:
                    texto_acumulado += formulario_base(f"sac_{id_chave}", f"Sacada de {nome_exibicao}")
            return texto_acumulado + "--- \n\n"
    return ""

relatorio_final = ""
st.header("2. Itens do Relatório")
relatorio_final += criar_secao_comodo("sala", "Sala", tem_sacada=True)
relatorio_final += criar_secao_comodo("cozinha", "Cozinha", tem_sacada=False)
relatorio_final += criar_secao_comodo("servico", "Área de Serviço", tem_sacada=False)
relatorio_final += criar_secao_comodo("banh_soc", "Banheiro Social", tem_sacada=False)
for n in range(1, num_dormitorios + 1):
    relatorio_final += criar_secao_comodo(f"dorm_{n}", f"Dormitório {n:02d}", tem_sacada=True)
for s in range(1, num_suites + 1):
    relatorio_final += criar_secao_comodo(f"suite_{s}", f"Suíte {s:02d}", tem_sacada=True, eh_suite=True)
relatorio_final += criar_secao_comodo("corredor", "Corredor", tem_sacada=False)
relatorio_final += criar_secao_comodo("escada", "Escada", tem_sacada=False)

st.divider()
st.header("📄 Relatório Gerado")
if relatorio_final:
    texto_limpo = relatorio_final.replace("**", "")
    st.text_area("Texto pronto para copiar:", texto_limpo, height=500)
    st.download_button("💾 Baixar Vistoria.txt", texto_limpo, file_name="vistoria.txt")
else:
    st.info("💡 Marque os cômodos acima para gerar a vistoria.")
