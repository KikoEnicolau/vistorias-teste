import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sistema de Vistoria Imobiliária", layout="wide")

# --- LINKS DIRETOS DAS IMAGENS (CORRIGIDOS) ---
# Extraídos diretamente para funcionarem no código
logo_url = "https://i.postimg.cc/9Myjqr69/Captura-de-tela-2026-02-24-160708.png" 
background_image_url = "https://i.postimg.cc/ZnJXBjF5/image.png"

# --- ESTILIZAÇÃO CSS PARA FUNDO E LOGO ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Caixa para o conteúdo ficar legível sobre o fundo */
    .block-container {{
        background-color: rgba(255, 255, 255, 0.92);
        padding: 30px !important;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-top: 50px;
        margin-bottom: 50px;
    }}

    /* Garante que os textos e etiquetas sejam pretos */
    h1, h2, h3, p, span, label, .stMarkdown {{
        color: #000000 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- EXIBIÇÃO DO LOGO ---
st.image(logo_url, width=250)

st.title("📋 Relatório de Vistoria de Imóveis")
st.write("Preencha os campos abaixo para gerar o relatório formatado.")

# --- LISTA DE CÔMODOS ---
comodos_config = [
    ("Sala", ["Sofá", "Mesa de centro", "Rack", "Televisão", "Interfone", "Mesa de madeira"]),
    ("Cozinha", ["Geladeira", "Cooktop", "Pia em Granito", "Gabinete", "Depurador de ar", "Forno Elétrico", "Micro-ondas", "Armário em MDF"]),
    ("Área de Serviço", ["Máquina de Lavar", "Tanque", "Armário", "Ralo de plástico"]),
    ("Banheiro Social", ["Vaso Sanitário", "Chuveiro", "Box", "Pia", "Gabinete", "Espelho", "Vitro", "Ralo"]),
    ("Suíte", ["Cama", "Guarda-roupa", "Ar Condicionado"]),
    ("Corredor", ["Caixa de Energia", "Escada"]),
    ("Dormitório 02", ["Cama", "Guarda-roupa"]),
    ("Banheiro Suíte", ["Vaso", "Chuveiro", "Pia", "Box", "Gabinete", "Espelho", "Vitro", "Ralo"]),
    ("Sacada/Cobertura", ["Jacuzzi", "Parapeito", "Soleira em granito"])
]

relatorio_completo = ""

for i, (nome, moveis) in enumerate(comodos_config, 1):
    with st.expander(f"{i}. {nome.upper()}"):
        incluir = st.checkbox(f"Incluir {nome}", key=f"check_{i}")
        
        if incluir:
            # PISO
            st.subheader("Piso e Rodapé")
            col1, col2 = st.columns(2)
            p_mat = col1.text_input("Tipo Piso", value="frio", key=f"p_mat_{i}")
            p_est = col2.selectbox("Estado", ["novo", "em bom estado", "usado"], key=f"p_est_{i}")
            p_obs = st.text_input("Observações do piso", key=f"p_obs_{i}")

            # PAREDE
            st.subheader("Paredes")
            col3, col4 = st.columns(2)
            par_tipo = col3.selectbox("Tipo", ["alvenaria", "azulejos até o teto"], key=f"par_tipo_{i}")
            par_est = col4.selectbox("Estado Parede", ["pintura nova", "pintura em bom estado", "pintura usada", "novos"], key=f"par_est_{i}")
            par_cor = st.text_input("Cor Parede", value="bege", key=f"par_cor_{i}")
            par_obs = st.text_input("Observações da parede", key=f"par_obs_{i}")

            # TETO
            st.subheader("Teto")
            col5, col6 = st.columns(2)
            t_mat = col5.text_input("Material Teto", value="gesso", key=f"t_mat_{i}")
            t_cor = col6.text_input("Cor Teto", value="branca", key=f"t_cor_{i}")
            col7, col8 = st.columns(2)
            t_mold = col7.selectbox("Moldura", ["com moldura de gesso", "sem moldura"], key=f"t_mold_{i}")
            t_est = col8.selectbox("Estado Teto", ["pintura nova", "pintura usada"], key=f"t_est_{i}")
            t_obs = st.text_input("Observações do teto", key=f"t_obs_{i}")

            # PORTA
            st.subheader("Porta")
            col9, col10 = st.columns(2)
            por_mat = col9.text_input("Material Porta", value="madeira", key=f"por_mat_{i}")
            por_cor = col10.text_input("Cor Porta", value="branca", key=f"por_cor_{i}")
            col11, col12 = st.columns(2)
            por_pint = col11.selectbox("Pintura Porta", ["pintura nova", "pintura usada", "envernizada nova", "envernizada usada"], key=f"por_pint_{i}")
            por_cond = col12.selectbox("Condição Porta", ["nova", "em bom estado", "usada"], key=f"por_cond_{i}")
            por_obs = st.text_input("Observações da porta", key=f"por_obs_{i}")

            # JANELA
            st.subheader("Janela")
            col13, col14 = st.columns(2)
            jan_mat = col13.text_input("Material Janela", value="alumínio", key=f"jan_mat_{i}")
            jan_est = col14.selectbox("Estado Janela", ["nova", "em bom estado", "usada"], key=f"jan_est_{i}")
            jan_obs = st.text_input("Observações da janela", key=f"jan_obs_{i}")

            # ELÉTRICA
            st.subheader("Tomadas e Interruptores")
            col15, col16 = st.columns(2)
            q_tom = col15.number_input("Qtd Tomadas", min_value=0, step=1, key=f"q_tom_{i}")
            q_int = col16.number_input("Qtd Interruptores", min_value=0, step=1, key=f"q_int_{i}")

            # MÓVEIS
            st.subheader("Móveis / Extras")
            lista_m_texto = []
            for m in moveis:
                m_cb = st.checkbox(m, key=f"m_cb_{m}_{i}")
                if m_cb:
                    m_obs = st.text_input(f"Detalhes: {m}", key=f"m_obs_{m}_{i}")
                    lista_m_texto.append(f"- {m}: {m_obs if m_obs else 'em bom estado'}")

            # --- CONSTRUÇÃO DO TEXTO ---
            txt = f"**{i}. {nome.upper()}**\n\n"
            txt += f"- Piso {p_mat} {p_est}, rodapé em piso {p_mat} {p_est}"
            if p_obs: txt += f", {p_obs}"
            txt += ".\n\n"
            
            txt += f"- Paredes em {par_tipo} na cor {par_cor}, {par_est}"
            if par_obs: txt += f". {par_obs}"
            txt += ".\n\n"
            
            txt += f"- Teto em {t_mat}, na cor {t_cor}, {t_mold}, {t_est}"
            if t_obs: txt += f", {t_obs}"
            txt += ".\n\n"
            
            txt += f"- Porta de {por_mat} {por_cond}, na cor {por_cor}, {por_pint}"
            if por_obs: txt += f", {por_obs}"
            txt += ".\n\n"
            
            txt += f"- Janela de {jan_mat} {jan_est}"
            if jan_obs: txt += f", {jan_obs}"
            txt += ".\n\n"
            
            elétrica = []
            if q_tom > 0:
                p_tom = "s" if q_tom > 1 else ""
                elétrica.append(f"{q_tom:02d} espelho{p_tom} tomadas de plástico em bom estado")
            if q_int > 0:
                p_int = "es" if q_int > 1 else ""
                elétrica.append(f"{q_int:02d} espelho{p_int} interruptor de plástico em bom estado")
            if elétrica: txt += f"- {' e '.join(elétrica)}.\n\n"
            
            if lista_m_texto:
                txt += "\n".join(lista_m_texto) + "\n\n"
            
            relatorio_completo += txt + "---\n\n"

st.divider()
st.header("📄 Relatório Final")
if relatorio_completo:
    st.text_area("Copie o texto abaixo:", relatorio_completo, height=400)
    st.download_button("Baixar Relatório (.txt)", relatorio_completo, file_name="vistoria.txt")
else:
    st.info("Selecione e preencha os cômodos acima para gerar o relatório.")
