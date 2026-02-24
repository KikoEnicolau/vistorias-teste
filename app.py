import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sistema de Vistoria Imobiliária", layout="wide")

# --- LINKS DAS IMAGENS ---
logo_url = "https://i.imgur.com/K6mE0K2.png" 
background_image_url = "https://i.imgur.com/1GvHpxq.jpeg"

# --- ESTILIZAÇÃO CSS ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .block-container {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 30px !important;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-top: 20px;
        max-width: 1000px;
    }}
    h1, h2, h3, p, span, label, .stMarkdown {{ color: #000000 !important; }}
    </style>
    """,
    unsafe_allow_html=True
)

st.image(logo_url, width=220)
st.title("📋 Vistoria Imobiliária Dinâmica")

# --- CONFIGURAÇÃO DO IMÓVEL ---
st.header("1. Configuração do Imóvel")
col_dorm, col_suit = st.columns(2)
num_dormitorios = col_dorm.number_input("Quantos Dormitórios (Simples)?", min_value=0, value=1, step=1)
num_suites = col_suit.number_input("Quantas Suítes?", min_value=0, value=0, step=1)

# --- FUNÇÃO PARA GERAR CAMPOS DE CÔMODO ---
def campos_comodo(id_chave, nome_exibicao, tem_sacada_opcional=True):
    with st.expander(f"{nome_exibicao.upper()}"):
        incluir = st.checkbox(f"Incluir {nome_exibicao}", key=f"check_{id_chave}")
        if incluir:
            st.subheader("Piso e Rodapé")
            c1, c2 = st.columns(2)
            p_mat = c1.text_input("Tipo Piso", value="frio", key=f"p_mat_{id_chave}")
            p_est = c2.selectbox("Estado", ["novo", "em bom estado", "usado"], key=f"p_est_{id_chave}")
            p_obs = st.text_input("Observações do piso", key=f"p_obs_{id_chave}")

            st.subheader("Paredes")
            c3, c4 = st.columns(2)
            par_tipo = c3.selectbox("Tipo", ["alvenaria", "azulejos até o teto"], key=f"par_tipo_{id_chave}")
            par_est = c4.selectbox("Estado Parede", ["pintura nova", "pintura em bom estado", "pintura usada"], key=f"par_est_{id_chave}")
            par_cor = st.text_input("Cor Parede", value="bege", key=f"par_cor_{id_chave}")
            par_obs = st.text_input("Observações da parede", key=f"par_obs_{id_chave}")

            st.subheader("Teto")
            c5, c6 = st.columns(2)
            t_mat = c5.text_input("Material Teto", value="gesso", key=f"t_mat_{id_chave}")
            t_cor = c6.text_input("Cor Teto", value="branca", key=f"t_cor_{id_chave}")
            c7, c8 = st.columns(2)
            t_mold = c7.selectbox("Moldura", ["com moldura de gesso", "sem moldura"], key=f"t_mold_{id_chave}")
            t_est = c8.selectbox("Estado Teto", ["pintura nova", "pintura usada"], key=f"t_est_{id_chave}")
            t_obs = st.text_input("Observações do teto", key=f"t_obs_{id_chave}")

            st.subheader("Porta")
            c9, c10 = st.columns(2)
            por_mat = c9.text_input("Material Porta", value="madeira", key=f"por_mat_{id_chave}")
            por_cor = c10.text_input("Cor Porta", value="branca", key=f"por_cor_{id_chave}")
            c11, c12 = st.columns(2)
            por_pint = c11.selectbox("Pintura Porta", ["pintura nova", "pintura usada", "envernizada"], key=f"por_pint_{id_chave}")
            por_cond = c12.selectbox("Condição Porta", ["nova", "em bom estado", "usada"], key=f"por_cond_{id_chave}")

            st.subheader("Janela")
            c13, c14 = st.columns(2)
            jan_mat = c13.text_input("Material Janela", value="alumínio", key=f"jan_mat_{id_chave}")
            jan_est = c14.selectbox("Estado Janela", ["nova", "em bom estado", "usada"], key=f"jan_est_{id_chave}")

            st.subheader("Elétrica")
            c15, c16 = st.columns(2)
            q_tom = c15.number_input("Qtd Tomadas", min_value=0, step=1, key=f"q_tom_{id_chave}")
            q_int = c16.number_input("Qtd Interruptores", min_value=0, step=1, key=f"q_int_{id_chave}")

            sacada_txt = ""
            if tem_sacada_opcional:
                st.subheader("Sacada")
                tem_sacada = st.checkbox("Este cômodo possui sacada?", key=f"sacada_check_{id_chave}")
                if tem_sacada:
                    sac_obs = st.text_input("Detalhes da Sacada (Piso, parapeito, vidro...)", key=f"sac_obs_{id_chave}")
                    sacada_txt = f"- Sacada: {sac_obs if sac_obs else 'em bom estado'}.\n\n"

            # Montagem do Texto
            txt = f"**{nome_exibicao.upper()}**\n\n"
            txt += f"- Piso {p_mat} {p_est}, rodapé em piso {p_mat} {p_est}"
            if p_obs: txt += f", {p_obs}"
            txt += ".\n\n"
            txt += f"- Paredes em {par_tipo} na cor {par_cor}, {par_est}. {par_obs}\n\n"
            txt += f"- Teto em {t_mat}, na cor {t_cor}, {t_mold}, {t_est}. {t_obs}\n\n"
            txt += f"- Porta de {por_mat} {por_cond}, na cor {por_cor}, {por_pint}.\n\n"
            txt += f"- Janela de {jan_mat} {jan_est}.\n\n"
            
            elétrica = []
            if q_tom > 0: elétrica.append(f"{q_tom:02d} espelhos tomadas de plástico em bom estado")
            if q_int > 0: elétrica.append(f"{q_int:02d} espelho interruptor de plástico em bom estado")
            if elétrica: txt += f"- {' e '.join(elétrica)}.\n\n"
            if sacada_txt: txt += sacada_txt
            
            return txt + "---\n\n"
    return ""

# --- EXECUÇÃO DOS CÔMODOS ---
relatorio_final = ""

st.header("2. Itens do Relatório")

# Fixos
relatorio_final += campos_comodo("sala", "Sala", tem_sacada_opcional=True)
relatorio_final += campos_comodo("cozinha", "Cozinha", tem_sacada_opcional=False)
relatorio_final += campos_comodo("servico", "Área de Serviço", tem_sacada_opcional=False)
relatorio_final += campos_comodo("banh_soc", "Banheiro Social", tem_sacada_opcional=False)

# Dinâmicos: Dormitórios
for n in range(1, num_dormitorios + 1):
    relatorio_final += campos_comodo(f"dorm_{n}", f"Dormitório {n:02d}", tem_sacada_opcional=True)

# Dinâmicos: Suítes
for s in range(1, num_suites + 1):
    relatorio_final += campos_comodo(f"suite_{s}", f"Suíte {s:02d}", tem_sacada_opcional=True)

# Outros Fixos
relatorio_final += campos_comodo("corredor", "Corredor", tem_sacada_opcional=False)
relatorio_final += campos_comodo("escada", "Escada", tem_sacada_opcional=False)

# --- ÁREA FINAL ---
st.divider()
st.header("📄 Relatório Gerado")
if relatorio_final:
    st.text_area("Texto formatado:", relatorio_final.replace("**", ""), height=400)
    st.download_button("Baixar TXT", relatorio_final.replace("**", ""), file_name="vistoria.txt")
else:
    st.info("Preencha e marque os cômodos para gerar o texto.")
