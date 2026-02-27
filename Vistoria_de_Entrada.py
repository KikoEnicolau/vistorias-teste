import streamlit as st

# Configuração da página
st.set_page_config(page_title="Vistoria Técnica Pro v3", page_icon="🏠", layout="centered")

# --- LISTAS DE OPÇÕES ---
OPCOES_ESTADO = ["Bom estado", "Novo", "Usado"]
OPCOES_CORES = ["Branca", "Gelo", "Cinza", "Bege", "Preta", "Marrom", "Amadeirada", "Off-white", "Natural"]
OPCOES_PISO_MAT = ["Frio", "Cerâmico", "Porcelanato", "Laminado", "Vinílico", "Ardósia", "Taco/Mad."]
OPCOES_RODAPE_MAT = OPCOES_PISO_MAT + ["Madeira/MDF", "Poliuretano", "PVC", "Poliestireno"]
OPCOES_RALO_MAT = ["Plástico", "Inox", "Ferro"]
OPCOES_MAT_PIA = ["Inox", "Granito", "Mármore", "Ardósia", "Sintético"]
OPCOES_MAT_CUBA = ["Inox", "Louça Branca", "Louça Bege", "Mesmo material da pia"]

# --- ESTILIZAÇÃO DA INTERFACE ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1a1a1a; color: white; }
    div[data-testid="stExpander"] { border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px; background-color: white; }
    h4 { color: #1a1a1a; border-bottom: 2px solid #eee; padding-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

def formulario_base(id_chave, nome_exibicao, eh_sacada=False):
    nome_lc = nome_exibicao.lower()
    if eh_sacada:
        titulo_secao = f"SACADA ({nome_exibicao.upper()})"
    else:
        titulo_secao = nome_exibicao.upper()
    
    with st.expander(f"📍 {titulo_secao}", expanded=False):
        texto_acumulado = ""

        # Auxiliares de gramática
        def fmt_est_m(est): return "em bom estado" if est == "Bom estado" else f"em estado {est.lower()}" if est == "Usado" else est.lower()
        def fmt_est_f(est):
            e = est.lower().replace("novo", "nova").replace("usado", "usada")
            return "com pintura em bom estado" if "bom" in e else f"com pintura {e}"
        def plural(qtd, singular, plural): return singular if qtd == 1 else plural

        # --- 1. PISO E RODAPÉ (LINHAS SEPARADAS) ---
        if st.checkbox("Incluir Piso/Rodapé?", key=f"inc_piso_{id_chave}"):
            st.markdown("#### 1. Piso e Rodapé")
            c1, c2, c3 = st.columns(3)
            p_mat = c1.selectbox("Material Piso", OPCOES_PISO_MAT, key=f"p_mat_{id_chave}")
            p_cor = c2.selectbox("Cor Piso", OPCOES_CORES, key=f"p_cor_{id_chave}")
            p_est = c3.selectbox("Estado Piso", OPCOES_ESTADO, key=f"p_est_{id_chave}")
            texto_acumulado += f"PISO: {p_mat} na cor {p_cor.lower()}, {fmt_est_m(p_est)}.\n"
            
            eh_area_fria = any(x in nome_lc for x in ["cozinha", "banheiro", "serviço", "lavanderia"])
            if not eh_area_fria or st.checkbox("Tem rodapé?", key=f"tem_roda_{id_chave}"):
                r1, r2, r3 = st.columns(3)
                r_mat = r1.selectbox("Material Rodapé", OPCOES_RODAPE_MAT, key=f"r_mat_{id_chave}")
                r_cor = r2.selectbox("Cor Rodapé", OPCOES_CORES, key=f"r_cor_{id_chave}")
                r_est = r3.selectbox("Estado Rodapé", OPCOES_ESTADO, key=f"r_est_{id_chave}")
                texto_acumulado += f"RODAPÉ: {r_mat} na cor {r_cor.lower()}, {fmt_est_m(r_est)}.\n"

        # --- 2. PAREDES E TETO (LINHAS SEPARADAS) ---
        if st.checkbox("Incluir Paredes/Teto?", key=f"inc_par_{id_chave}"):
            st.markdown("---")
            st.markdown("#### 2. Paredes e Teto")
            tipo_p = st.radio("Tipo de Parede:", ["Alvenaria", "Azulejos", "Meia Parede"], key=f"tipo_p_{id_chave}", horizontal=True)
            
            if tipo_p == "Alvenaria":
                c1, c2 = st.columns(2)
                p_cor = c1.selectbox("Cor Parede", OPCOES_CORES, key=f"p_cor_a_{id_chave}")
                p_est = c2.selectbox("Estado Parede", OPCOES_ESTADO, key=f"p_est_a_{id_chave}")
                texto_acumulado += f"PAREDES: Cor {p_cor.lower()} {fmt_est_f(p_est)}.\n"
            elif tipo_p == "Azulejos":
                azu_est = st.selectbox("Estado Azulejos", OPCOES_ESTADO, key=f"azu_est_{id_chave}")
                texto_acumulado += f"PAREDES: Com revestimento de azulejos até o teto {fmt_est_m(azu_est)}.\n"
            else:
                m1, m2, m3 = st.columns(3)
                texto_acumulado += f"PAREDES: Sendo metade de baixo com revestimento de azulejos {fmt_est_m(m1.selectbox('Azulejo', OPCOES_ESTADO, key=f'm_a_{id_chave}'))} e metade de cima em alvenaria na cor {m2.selectbox('Cor', OPCOES_CORES, key=f'm_c_{id_chave}').lower()} {fmt_est_f(m3.selectbox('Estado', OPCOES_ESTADO, key=f'm_e_{id_chave}'))}.\n"
            
            t1, t2 = st.columns(2)
            texto_acumulado += f"TETO: Cor {t1.selectbox('Cor Teto', OPCOES_CORES, key=f't_c_{id_chave}').lower()} {fmt_est_f(t2.selectbox('Estado Teto', OPCOES_ESTADO, key=f't_e_{id_chave}'))}.\n"

        # --- 3. PIA E GABINETE (EXCLUSIVO COZINHA/BANHEIRO) ---
        if any(x in nome_lc for x in ["cozinha", "banheiro"]):
            st.markdown("---")
            st.markdown("#### 3. Itens de Bancada")
            if st.checkbox("Incluir Pia?", key=f"inc_pia_{id_chave}"):
                c1, c2, c3 = st.columns(3)
                p_mat = c1.selectbox("Material Pia", OPCOES_MAT_PIA, key=f"pia_mat_{id_chave}")
                p_cuba = c2.selectbox("Material Cuba", OPCOES_MAT_CUBA, key=f"pia_cuba_{id_chave}")
                p_est = c3.selectbox("Estado Pia", OPCOES_ESTADO, key=f"pia_est_{id_chave}")
                texto_acumulado += f"PIA: Em {p_mat.lower()} com cuba de {p_cuba.lower()}, {fmt_est_m(p_est)}.\n"
            
            if st.checkbox("Incluir Gabinete?", key=f"inc_gab_{id_chave}"):
                g1, g2, g3 = st.columns(3)
                g_mat = g1.selectbox("Material Gabinete", ["Madeira/MDF", "Metal", "PVC"], key=f"gab_mat_{id_chave}")
                g_portas = g2.number_input("Qtd Portas", 0, 10, key=f"gab_p_{id_chave}")
                g_gavetas = g3.number_input("Qtd Gavetas", 0, 10, key=f"gab_g_{id_chave}")
                g_pux = st.radio("Puxadores?", ["Em bom estado", "Faltantes", "Oxidados", "Não possui"], key=f"gab_pux_{id_chave}", horizontal=True)
                g_est = st.selectbox("Estado Geral Gabinete", OPCOES_ESTADO, key=f"gab_est_{id_chave}")
                texto_acumulado += f"GABINETE: Em {g_mat.lower()} com {g_portas} {plural(g_portas, 'porta', 'portas')} e {g_gavetas} {plural(g_gavetas, 'gaveta', 'gavetas')}. Puxadores {g_pux.lower()}, móvel {fmt_est_m(g_est)}.\n"

        # --- 4. PORTAS E JANELAS ---
        if st.checkbox("Incluir Porta/Janela?", key=f"inc_pj_{id_chave}"):
            st.markdown("---")
            st.markdown("#### 4. Aberturas")
            colp1, colp2 = st.columns(2)
            p_mat = colp1.selectbox("Material Porta", ["Madeira", "Alumínio", "Ferro", "PVC"], key=f"por_mat_{id_chave}")
            p_est = colp2.selectbox("Estado Porta", OPCOES_ESTADO, key=f"por_est_{id_chave}")
            fec = st.text_input("Fechadura / Maçaneta (Ex: Maçaneta tipo alavanca inox, fechadura funcionando)", key=f"fec_{id_chave}")
            texto_acumulado += f"PORTA: {p_mat} {fmt_est_m(p_est)}. {fec}.\n"
            
            st.write("Janela:")
            j1, j2, j3 = st.columns(3)
            j_mat = j1.selectbox("Material Janela", ["Alumínio", "Madeira", "Ferro"], key=f"jan_mat_{id_chave}")
            j_est = j2.selectbox("Estado Janela", OPCOES_ESTADO, key=f"jan_est_{id_chave}")
            v_est = j3.selectbox("Estado Vidros", OPCOES_ESTADO, key=f"vid_est_{id_chave}")
            j4, j5 = st.columns(2)
            q_v = j4.number_input("Qtd Vidros", 0, 20, value=1, key=f"qv_{id_chave}")
            q_t = j5.number_input("Qtd Trincos", 0, 10, value=1, key=f"qt_{id_chave}")
            texto_acumulado += f"JANELA: {j_mat} em {fmt_est_m(j_est)} com {q_t} {plural(q_t, 'trinco', 'trincos')} e {q_v:02} {plural(q_v, 'vidro', 'vidros')} {fmt_est_m(v_est)}.\n"

        # --- 5. ELÉTRICA, ILUMINAÇÃO E RALO ---
        if st.checkbox("Incluir Elétrica/Ralo?", key=f"inc_er_{id_chave}"):
            st.markdown("---")
            st.markdown("#### 5. Complementos")
            # Iluminação Pluralizada
            il1, il2 = st.columns(2)
            tipo_il = il1.selectbox("Tipo Iluminação", ["Plafon", "Spot", "Luminária led", "Lâmpada dicroica"], key=f"tilu_{id_chave}")
            qtd_il = il2.number_input("Quantidade", 1, 20, key=f"qilu_{id_chave}")
            est_il = st.selectbox("Estado Iluminação", OPCOES_ESTADO, key=f"eilu_{id_chave}")
            texto_acumulado += f"ILUMINAÇÃO: {qtd_il:02} {plural(qtd_il, tipo_il.lower(), tipo_il.lower()+'s')} {fmt_est_m(est_il)}.\n"
            
            # Ralo Pluralizado
            ra1, ra2, ra3 = st.columns(3)
            r_mat = ra1.selectbox("Material Ralo", OPCOES_RALO_MAT, key=f"rmat_{id_chave}")
            r_qtd = ra2.number_input("Qtd Ralos", 1, 10, key=f"rqtd_{id_chave}")
            r_est = ra3.selectbox("Estado Ralo", OPCOES_ESTADO, key=f"rest_{id_chave}")
            texto_acumulado += f"RALO: {r_qtd:02} {plural(r_qtd, 'ralo', 'ralos')} de {r_mat.lower()} {fmt_est_m(r_est)}.\n"

    return f"\n{titulo_secao}\n{texto_acumulado}"

# --- APP PRINCIPAL ---
st.title("📋 Vistoria Profissional")

col1, col2 = st.columns(2)
q_quartos = col1.number_input("Quantos Quartos?", 0, 10, 1)
q_suites = col2.number_input("Quantas Suítes?", 0, 10, 0)
outras_areas = st.multiselect("Outras Áreas:", ["Sala", "Cozinha", "Banheiro Social", "Área de Serviço", "Sacada da Sala", "Garagem"], default=["Sala", "Cozinha"])

relatorio_txt = ""

if "Sala" in outras_areas: relatorio_txt += formulario_base("sala", "Sala")
if "Sacada da Sala" in outras_areas: relatorio_txt += formulario_base("sac_sala", "Sala", eh_sacada=True)

for i in range(q_quartos): relatorio_txt += formulario_base(f"q{i}", f"Quarto {i+1}")
for i in range(q_suites):
    relatorio_txt += formulario_base(f"sq{i}", f"Quarto da Suíte {i+1}")
    relatorio_txt += formulario_base(f"sb{i}", f"Banheiro da Suíte {i+1}")

if "Cozinha" in outras_areas: relatorio_txt += formulario_base("coz", "Cozinha")
if "Banheiro Social" in outras_areas: relatorio_txt += formulario_base("bsoc", "Banheiro Social")
if "Área de Serviço" in outras_areas: relatorio_txt += formulario_base("aserv", "Área de Serviço")

# --- EXPORTAÇÃO ---
st.header("📄 Relatório")
if relatorio_txt:
    st.text_area("Pré-visualização (Texto Simples):", relatorio_txt, height=300)
    
    # Gerador de HTML para abrir no Word com as fontes corretas
    html_formatado = f"""
    <html>
    <head><style>
        body {{ font-family: 'Times New Roman', Times, serif; font-size: 12pt; color: black; line-height: 1.5; }}
        h3 {{ font-size: 14pt; font-weight: bold; text-transform: uppercase; margin-top: 20px; border-bottom: 1px solid black; }}
    </style></head>
    <body>
        {relatorio_txt.replace('\n', '<br>').replace('### ', '<h3>').replace('📍 ', '<h3>')}
    </body>
    </html>
    """
    
    st.download_button(
        label="📥 Baixar para Word (Times New Roman 12)",
        data=html_formatado,
        file_name="vistoria_final.doc",
        mime="application/msword"
    )
