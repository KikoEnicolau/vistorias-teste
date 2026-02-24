import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sistema de Vistoria Imobiliária", layout="wide")

# --- LINKS DAS IMAGENS ---
logo_url = "https://i.postimg.cc/9Myjqr69/Captura-de-tela-2026-02-24-160708.png" 
# Substitua os links abaixo pelas fotos que você deseja nas laterais
foto_esquerda = "https://i.postimg.cc/ZnJXBjF5/image.png" # Exemplo: Foto de uma sala
foto_direita = "https://i.postimg.cc/XvnbywK0/image.png"  # Exemplo: Foto de uma fachada

# --- ESTILIZAÇÃO CSS (LATERAIS) ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background: 
            url("{foto_esquerda}") left center / 25% no-repeat fixed,
            url("{foto_direita}") right center / 25% no-repeat fixed,
            #f0f2f6; /* Cor de fundo caso as imagens não carreguem */
    }}
    
    /* Centraliza e organiza o corpo do formulário */
    .block-container {{
        background-color: rgba(255, 255, 255, 0.98);
        padding: 40px !important;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        max-width: 850px; /* Largura ideal para sobrar espaço nas fotos laterais */
        margin: auto;
        border: 1px solid #ddd;
    }}

    /* Ajuste para telas de celular (esconde as fotos laterais para não esmagar o texto) */
    @media (max-width: 768px) {{
        .stApp {{
            background: #ffffff;
        }}
        .block-container {{
            max-width: 95%;
            padding: 15px !important;
        }}
    }}

    h1, h2, h3, p, span, label, .stMarkdown {{ color: #000000 !important; }}
    </style>
    """,
    unsafe_allow_html=True
)

st.image(logo_url, width=220)
st.title("📋 Vistoria Imobiliária Dinâmica")

# --- 1. CONFIGURAÇÃO DO IMÓVEL ---
st.header("1. Configuração do Imóvel")
col_dorm, col_suit = st.columns(2)
num_dormitorios = col_dorm.number_input("Quantos Dormitórios (Simples)?", min_value=0, value=1, step=1)
num_suites = col_suit.number_input("Quantas Suítes?", min_value=0, value=0, step=1)

# --- FUNÇÃO AUXILIAR PARA CÔMODOS COMPLETOS ---
def formulario_base(id_chave, nome_exibicao):
    st.markdown(f"**Configuração de {nome_exibicao}**")
    
    # PISO
    c1, c2 = st.columns(2)
    p_mat = c1.text_input("Tipo Piso", value="frio", key=f"p_mat_{id_chave}")
    p_est = c2.selectbox("Estado Piso", ["novo", "em bom estado", "usado"], key=f"p_est_{id_chave}")
    p_obs = st.text_input("Obs. Piso (ex: riscos)", key=f"p_obs_{id_chave}")

    # PAREDE
    c3, c4 = st.columns(2)
    par_tipo = c3.selectbox("Tipo Parede", ["alvenaria", "azulejos até o teto"], key=f"par_tipo_{id_chave}")
    par_est = c4.selectbox("Estado Parede", ["pintura nova", "pintura em bom estado", "pintura usada"], key=f"par_est_{id_chave}")
    par_cor = st.text_input("Cor Parede", value="bege", key=f"par_cor_{id_chave}")
    par_obs = st.text_input("Obs. Parede", key=f"par_obs_{id_chave}")

    # TETO
    c5, c6 = st.columns(2)
    t_mat = c5.text_input("Material Teto", value="gesso", key=f"t_mat_{id_chave}")
    t_cor = c6.text_input("Cor Teto", value="branca", key=f"t_cor_{id_chave}")
    c7, c8 = st.columns(2)
    t_mold = c7.selectbox("Moldura", ["com moldura de gesso", "sem moldura"], key=f"t_mold_{id_chave}")
    t_est = c8.selectbox("Estado Teto", ["pintura nova", "pintura usada"], key=f"t_est_{id_chave}")
    t_obs = st.text_input("Obs. Teto (Iluminação/Lâmpadas)", key=f"t_obs_{id_chave}")

    # PORTA (Opcional para Sacadas)
    porta_txt = ""
    if "sacada" not in id_chave:
        st.markdown("---")
        c9, c10 = st.columns(2)
        por_mat = c9.text_input("Material Porta", value="madeira", key=f"por_mat_{id_chave}")
        por_cor = c10.text_input("Cor Porta", value="branca", key=f"por_cor_{id_chave}")
        c11, c12 = st.columns(2)
        por_pint = c11.selectbox("Pintura Porta", ["pintura nova", "pintura usada", "envernizada"], key=f"por_pint_{id_chave}")
        por_cond = c12.selectbox("Condição Porta", ["nova", "em bom estado", "usada"], key=f"por_cond_{id_chave}")
        por_obs = st.text_input("Obs. Porta", key=f"por_obs_{id_chave}")
        porta_txt = f"- Porta de {por_mat} {por_cond}, na cor {por_cor}, {por_pint}. {por_obs}\n\n"

    # JANELA
    st.markdown("---")
    c13, c14 = st.columns(2)
    jan_mat = c13.text_input("Material Janela", value="alumínio", key=f"jan_mat_{id_chave}")
    jan_est = c14.selectbox("Estado Janela", ["nova", "em bom estado", "usada"], key=f"jan_est_{id_chave}")
    jan_obs = st.text_input("Obs. Janela (Vidros, trancas, telas)", key=f"jan_obs_{id_chave}")

    # ELÉTRICA
    st.markdown("---")
    c15, c16 = st.columns(2)
    q_tom = c15.number_input("Qtd Tomadas", min_value=0, step=1, key=f"q_tom_{id_chave}")
    q_int = c16.number_input("Qtd Interruptores", min_value=0, step=1, key=f"q_int_{id_chave}")

    # Formatação do texto
    res = f"**{nome_exibicao.upper()}**\n"
    res += f"- Piso {p_mat} {p_est}, rodapé em piso {p_mat} {p_est}. {p_obs}\n"
    res += f"- Paredes em {par_tipo} na cor {par_cor}, {par_est}. {par_obs}\n"
    res += f"- Teto em {t_mat}, na cor {t_cor}, {t_mold}, {t_est}. {t_obs}\n"
    if porta_txt: res += porta_txt
    res += f"- Janela de {jan_mat} {jan_est}. {jan_obs}\n"
    
    elet = []
    if q_tom > 0: elet.append(f"{q_tom:02d} espelhos tomadas de plástico em bom estado")
    if q_int > 0: elet.append(f"{q_int:02d} espelho interruptor de plástico em bom estado")
    if elet: res += f"- {' e '.join(elet)}.\n"
    
    return res + "\n"

# --- FUNÇÃO PARA GERAR CÔMODOS DINÂMICOS ---
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

# --- 2. EXECUÇÃO DOS CÔMODOS ---
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

# --- 3. ÁREA FINAL ---
st.divider()
st.header("📄 Relatório Gerado")
if relatorio_final:
    texto_limpo = relatorio_final.replace("**", "")
    st.text_area("Texto pronto para copiar:", texto_limpo, height=500)
    st.download_button("💾 Baixar Vistoria.txt", texto_limpo, file_name="vistoria.txt")
else:
    st.info("💡 Marque os cômodos acima para gerar a vistoria.")
