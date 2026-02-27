import streamlit as st

# Configuração da página
st.set_page_config(page_title="Vistoria Técnica Pro v10", page_icon="🏠", layout="centered")

# --- LISTAS DE OPÇÕES ---
OPCOES_ESTADO = ["em bom estado", "novo", "usado"]
OPCOES_CORES = ["branca", "gelo", "cinza", "bege", "preta", "marrom", "amadeirada", "off-white", "natural"]
OPCOES_PISO_MAT = ["frio", "cerâmico", "porcelanato", "laminado", "vinílico", "ardósia", "taco/mad."]
OPCOES_RODAPE_MAT = OPCOES_PISO_MAT + ["madeira/mdf", "poliuretano", "pvc", "poliestireno"]
OPCOES_RALO_MAT = ["plástico", "inox", "ferro"]
OPCOES_MAT_PIA = ["inox", "granito", "mármore", "ardósia", "sintético", "vidro"]
OPCOES_MAT_CUBA = ["inox", "louça branca", "louça bege", "vidro", "mesmo material da pia"]
OPCOES_MAT_SPOT = ["plástico", "alumínio", "ferro"]

# --- ESTILIZAÇÃO ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1a1a1a; color: white; }
    div[data-testid="stExpander"] { border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px; background-color: white; }
    h4 { color: #1a1a1a; border-bottom: 2px solid #eee; padding-bottom: 5px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

def formulario_base(id_chave, nome_exibicao, eh_sacada=False):
    nome_lc = nome_exibicao.lower()
    titulo_secao = f"SACADA ({nome_exibicao.upper()})" if eh_sacada else nome_exibicao.upper()
    
    with st.expander(f"📍 {titulo_secao}", expanded=False):
        texto_acumulado = ""

        def plural(qtd, singular, plural): return singular if qtd <= 1 else plural

        # --- 1. PISO E RODAPÉ ---
        if st.checkbox("Incluir Piso/Rodapé?", key=f"inc_piso_{id_chave}"):
            st.markdown("#### 1. Piso e Rodapé")
            c1, c2, c3 = st.columns(3)
            p_mat = c1.selectbox("Material Piso", OPCOES_PISO_MAT, key=f"p_mat_{id_chave}")
            p_cor = c2.selectbox("Cor Piso", OPCOES_CORES, key=f"p_cor_{id_chave}")
            p_est = c3.selectbox("Estado Piso", OPCOES_ESTADO, key=f"p_est_{id_chave}")
            texto_acumulado += f"- Piso {p_mat} na cor {p_cor}, {p_est}.\n"
            
            if not any(x in nome_lc for x in ["cozinha", "banheiro", "serviço"]) or st.checkbox("Tem rodapé?", key=f"tem_roda_{id_chave}"):
                r1, r2, r3 = st.columns(3)
                r_mat = r1.selectbox("Material Rodapé", OPCOES_RODAPE_MAT, key=f"r_mat_{id_chave}")
                r_cor = r2.selectbox("Cor Rodapé", OPCOES_CORES, key=f"r_cor_{id_chave}")
                r_est = r3.selectbox("Estado Rodapé", OPCOES_ESTADO, key=f"r_est_{id_chave}")
                texto_acumulado += f"- Rodapé em {r_mat} na cor {r_cor}, {r_est}.\n"

        # --- 2. PAREDES E TETO ---
        if st.checkbox("Incluir Paredes/Teto?", key=f"inc_par_{id_chave}"):
            st.markdown("---")
            st.markdown("#### 2. Paredes e Teto")
            tipo_p = st.radio("Parede:", ["Alvenaria", "Azulejos"], key=f"tipo_p_{id_chave}", horizontal=True)
            if tipo_p == "Alvenaria":
                c1, c2 = st.columns(2)
                pc, pe = c1.selectbox("Cor Parede", OPCOES_CORES, key=f"pc_{id_chave}"), c2.selectbox("Estado Parede", OPCOES_ESTADO, key=f"pe_{id_chave}")
                texto_acumulado += f"- Paredes na cor {pc}, {pe}.\n"
            else:
                az = st.selectbox("Estado Azulejo", OPCOES_ESTADO, key=f"az_{id_chave}")
                texto_acumulado += f"- Paredes com revestimento de azulejos {az}.\n"
            
            c_t1, c_t2 = st.columns(2)
            t_cor, t_est = c_t1.selectbox("Cor Teto", OPCOES_CORES, key=f"tc_{id_chave}"), c_t2.selectbox("Estado Teto", OPCOES_ESTADO, key=f"te_{id_chave}")
            gesso = st.checkbox("Tem moldura de gesso?", key=f"gesso_{id_chave}")
            txt_gesso = " com moldura de gesso" if gesso else " sem moldura"
            texto_acumulado += f"- Teto na cor {t_cor}, {t_est}{txt_gesso}.\n"

        # --- 3. PIA E GABINETE ---
        if any(x in nome_lc for x in ["cozinha", "banheiro"]):
            st.markdown("---")
            st.markdown("#### 3. Itens de Bancada")
            if st.checkbox("Incluir Pia?", key=f"inc_pia_{id_chave}"):
                c1, c2, c3 = st.columns(3)
                pm, cm, pse = c1.selectbox("Pia", OPCOES_MAT_PIA, key=f'pm_{id_chave}'), c2.selectbox("Cuba", OPCOES_MAT_CUBA, key=f'cm_{id_chave}'), c3.selectbox("Est. Pia", OPCOES_ESTADO, key=f'pse_{id_chave}')
                texto_acumulado += f"- Pia em {pm} com cuba de {cm}, {pse}.\n"
            if st.checkbox("Incluir Gabinete?", key=f"inc_gab_{id_chave}"):
                g1, g2, g3 = st.columns(3)
                gp, gg, ge = g1.number_input("Portas", 0, 10, key=f'gp_{id_chave}'), g2.number_input("Gavetas", 0, 10, key=f'gg_{id_chave}'), g3.selectbox("Est. Gabinete", OPCOES_ESTADO, key=f'ge_{id_chave}')
                texto_acumulado += f"- Gabinete com {gp} {plural(gp, 'porta', 'portas')} e {gg} {plural(gg, 'gaveta', 'gavetas')}, {ge}.\n"

        # --- 4. PORTA ---
        if st.checkbox("Incluir Porta?", key=f"inc_por_{id_chave}"):
            st.markdown("---")
            st.markdown("#### 4. Porta")
            c1, c2 = st.columns(2)
            p_mat, p_est = c1.selectbox("Material Porta", ["madeira", "alumínio", "ferro"], key=f"pm_p_{id_chave}"), c2.selectbox("Estado Porta", OPCOES_ESTADO, key=f"pe_p_{id_chave}")
            c3, c4, c5 = st.columns(3)
            be, me, fe = c3.selectbox("Batente", OPCOES_ESTADO, key=f"be_{id_chave}"), c4.selectbox("Maçaneta", OPCOES_ESTADO, key=f"me_{id_chave}"), c5.selectbox("Fechadura", OPCOES_ESTADO, key=f"fe_{id_chave}")
            tem_chave = st.checkbox("Tem chave?", key=f"tem_ch_{id_chave}")
            qtd_ch = st.number_input("Qtd chaves", 0, 10, key=f"qtd_ch_{id_chave}") if tem_chave else 0
            txt_ch = f", acompanhada de {qtd_ch} {plural(qtd_ch, 'chave', 'chaves')}" if tem_chave else ", sem chave"
            texto_acumulado += f"- Porta de {p_mat} {p_est}, batente {be}, maçaneta {me} e fechadura {fe}{txt_ch}.\n"

        # --- 5. JANELA ---
        if st.checkbox("Incluir Janela?", key=f"inc_jan_{id_chave}"):
            cj1, cj2, cj3 = st.columns(3)
            j_mat, j_est, v_est = cj1.selectbox("Material", ["alumínio", "ferro"], key=f"jm_{id_chave}"), cj2.selectbox("Estado", OPCOES_ESTADO, key=f"je_{id_chave}"), cj3.selectbox("Vidros", OPCOES_ESTADO, key=f"ve_{id_chave}")
            cj4, cj5 = st.columns(2)
            qv, qt = cj4.number_input("Qtd Vidros", 1, 20, key=f"qv_{id_chave}"), cj5.number_input("Qtd Trincos", 1, 10, key=f"qt_{id_chave}")
            texto_acumulado += f"- Janela de {j_mat} {j_est} com {qt} {plural(qt, 'trinco', 'trincos')} e {qv:02} {plural(qv, 'vidro', 'vidros')} {v_est}.\n"

        # --- 6. ILUMINAÇÃO ---
        if st.checkbox("Incluir Iluminação?", key=f"inc_ilu_{id_chave}"):
            st.markdown("---")
            st.markdown("#### 5. Iluminação")
            t_ilu = st.selectbox("Tipo", ["plafon", "spot", "luminária led"], key=f"til_{id_chave}")
            c1, c2, c3 = st.columns(3)
            q_ilu = c1.number_input("Qtd Itens", 1, 20, key=f"qilu_{id_chave}")
            e_ilu = c2.selectbox("Estado Item", OPCOES_ESTADO, key=f"eilu_{id_chave}")
            q_lamp = c3.number_input("Qtd Lâmpadas", 1, 10, key=f"qlamp_{id_chave}")
            f_lamp = st.radio("Status Lâmpada", ["funcionando", "queimada", "faltante"], key=f"flamp_{id_chave}", horizontal=True)
            
            detalhe = "de vidro " if t_ilu == "plafon" else f"de {st.selectbox('Material Spot', OPCOES_MAT_SPOT, key=f'mspot_{id_chave}')} " if t_ilu == "spot" else ""
            texto_acumulado += f"- {q_ilu:02} {plural(q_ilu, t_ilu, t_ilu+'s')} {detalhe}{e_ilu}, com {q_lamp:02} {plural(q_lamp, 'lâmpada', 'lâmpadas')} {f_lamp}.\n"

        # --- 7. ELÉTRICA ---
        if st.checkbox("Incluir Elétrica?", key=f"inc_ele_{id_chave}"):
            st.markdown("#### 6. Elétrica")
            c1, c2, c3 = st.columns(3)
            tom, inter, ee = c1.number_input('Espelhos Tomada', 0, 50, key=f't_{id_chave}'), c2.number_input('Interruptores', 0, 50, key=f'i_{id_chave}'), c3.selectbox('Est. Geral', OPCOES_ESTADO, key=f'ee_{id_chave}')
            
            txt_tom = f"{tom:02} {plural(tom, 'espelho tomada', 'espelhos tomadas')}"
            txt_int = f"{inter:02} {plural(inter, 'interruptor', 'interruptores')}"
            texto_acumulado += f"- {txt_tom} e {txt_int} {ee}.\n"
            
            if st.checkbox("Incluir Quadro de Disjuntores?", key=f"inc_quad_{id_chave}"):
                qc1, qc2 = st.columns(2)
                texto_acumulado += f"- Quadro de disjuntores em {qc1.selectbox('Material', ['plástico', 'metal'], key=f'qm_{id_chave}')} {qc2.selectbox('Estado', OPCOES_ESTADO, key=f'qe_{id_chave}')}.\n"

        # --- 8. RALO ---
        if st.checkbox("Incluir Ralo?", key=f"inc_ral_{id_chave}"):
            cr1, cr2 = st.columns(2)
            rm, rq = cr1.selectbox("Material Ralo", OPCOES_RALO_MAT, key=f"rm_{id_chave}"), cr2.number_input("Qtd Ralos", 1, 10, key=f"rq_{id_chave}")
            texto_acumulado += f"- {rq:02} {plural(rq, 'unidade de ralo', 'unidades de ralo')} de {rm} em bom estado.\n"

    return f"\n{titulo_secao}\n{texto_acumulado}"

# --- APP PRINCIPAL ---
st.title("📋 Vistoria Profissional")
q_q, q_s = st.columns(2)
num_q, num_s = q_q.number_input("Quartos", 0, 10, 1), q_s.number_input("Suítes", 0, 10, 0)
areas = st.multiselect("Áreas:", ["Sala", "Corredor", "Cozinha", "Banheiro Social", "Área de Serviço"], default=["Sala", "Cozinha"])

relatorio = ""
# Ordem de geração
if "Sala" in areas:
    relatorio += formulario_base("sala", "Sala")
    if st.checkbox("A Sala possui sacada?"): relatorio += formulario_base("sac_sala", "Sala", eh_sacada=True)
if "Corredor" in areas: relatorio += formulario_base("corredor", "Corredor")
for i in range(num_q):
    relatorio += formulario_base(f"q{i}", f"Quarto {i+1}")
    if st.checkbox(f"O Quarto {i+1} possui sacada?", key=f"chk_sq{i}"): relatorio += formulario_base(f"sac_q{i}", f"Quarto {i+1}", eh_sacada=True)
for i in range(num_s):
    relatorio += formulario_base(f"sq{i}", f"Quarto Suíte {i+1}")
    if st.checkbox(f"A Suíte {i+1} possui sacada?", key=f"chk_ss{i}"): relatorio += formulario_base(f"sac_s{i}", f"Suíte {i+1}", eh_sacada=True)
    relatorio += formulario_base(f"sb{i}", f"Banheiro Suíte {i+1}")
if "Cozinha" in areas: relatorio += formulario_base("coz", "Cozinha")
if "Banheiro Social" in areas: relatorio += formulario_base("bsoc", "Banheiro Social")
if "Área de Serviço" in areas: relatorio += formulario_base("aserv", "Área de Serviço")

if relatorio:
    st.header("📄 Relatório Final")
    st.text_area("Texto:", relatorio, height=250)
    
    # --- O SEGREDO PARA OS ACENTOS NO WORD ---
    html_word = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Times New Roman', serif; font-size: 12pt; color: black; line-height: 1.2; }}
        </style>
    </head>
    <body>
        {relatorio.replace('\n', '<br>')}
    </body>
    </html>
    """
    
    st.download_button(
        label="📥 Baixar Vistoria para Word",
        data=html_word,
        file_name="vistoria_tecnica.doc",
        mime="application/msword"
    )
