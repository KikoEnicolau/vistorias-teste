import streamlit as st

# Configuração da página para parecer um App no celular
st.set_page_config(page_title="Vistoria Pro", page_icon="🏠", layout="centered")

# --- LISTAS DE OPÇÕES ---
OPCOES_ESTADO = ["em bom estado", "novo", "usado", "com avarias"]
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
    .stButton>button { height: 3em; font-weight: bold; border-radius: 10px; }
    div[data-testid="stExpander"] { border-radius: 12px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

def formulario_base(id_chave, nome_exibicao, eh_sacada=False):
    nome_lc = nome_exibicao.lower()
    titulo_secao = f"SACADA ({nome_exibicao.upper()})" if eh_sacada else nome_exibicao.upper()
    
    with st.expander(f"📍 {titulo_secao}", expanded=False):
        texto_acumulado = ""
        def plural(qtd, singular, plural): return singular if qtd <= 1 else plural

        # 1. PISO E RODAPÉ
        if st.checkbox("Piso/Rodapé", key=f"inc_piso_{id_chave}"):
            c1, c2, c3 = st.columns(3)
            p_mat, p_cor, p_est = c1.selectbox("Material", OPCOES_PISO_MAT, key=f"p_mat_{id_chave}"), c2.selectbox("Cor", OPCOES_CORES, key=f"p_cor_{id_chave}"), c3.selectbox("Estado", OPCOES_ESTADO, key=f"p_est_{id_chave}")
            texto_acumulado += f"- Piso {p_mat} na cor {p_cor}, {p_est}.\n"
            
            if not any(x in nome_lc for x in ["cozinha", "banheiro", "serviço"]) or st.checkbox("Tem rodapé?", key=f"tem_roda_{id_chave}"):
                r1, r2, r3 = st.columns(3)
                r_mat, r_cor, r_est = r1.selectbox("Mat. Rodapé", OPCOES_RODAPE_MAT, key=f"r_mat_{id_chave}"), r2.selectbox("Cor Rodapé", OPCOES_CORES, key=f"r_cor_{id_chave}"), r3.selectbox("Est. Rodapé", OPCOES_ESTADO, key=f"r_est_{id_chave}")
                texto_acumulado += f"- Rodapé em {r_mat} na cor {r_cor}, {r_est}.\n"

        # 2. PAREDES E TETO
        if st.checkbox("Paredes/Teto", key=f"inc_par_{id_chave}"):
            tipo_p = st.radio("Parede:", ["Alvenaria", "Azulejos"], key=f"tipo_p_{id_chave}", horizontal=True)
            if tipo_p == "Alvenaria":
                c1, c2 = st.columns(2)
                texto_acumulado += f"- Paredes na cor {c1.selectbox('Cor', OPCOES_CORES, key=f'pc_{id_chave}')}, {c2.selectbox('Estado', OPCOES_ESTADO, key=f'pe_{id_chave}')}.\n"
            else:
                texto_acumulado += f"- Paredes com revestimento de azulejos {st.selectbox('Estado', OPCOES_ESTADO, key=f'az_{id_chave}')}.\n"
            
            t_cor, t_est = st.columns(2)
            gesso = st.checkbox("Moldura de gesso?", key=f"gesso_{id_chave}")
            texto_acumulado += f"- Teto na cor {t_cor.selectbox('Cor Teto', OPCOES_CORES, key=f'tc_{id_chave}')}, {t_est.selectbox('Est. Teto', OPCOES_ESTADO, key=f'te_{id_chave}')}{' com moldura de gesso' if gesso else ' sem moldura'}.\n"

        # 3. PORTA
        if st.checkbox("Porta", key=f"inc_por_{id_chave}"):
            c1, c2 = st.columns(2)
            p_mat, p_est = c1.selectbox("Material", ["madeira", "alumínio", "ferro"], key=f"pm_p_{id_chave}"), c2.selectbox("Estado", OPCOES_ESTADO, key=f"pe_p_{id_chave}")
            c3, c4, c5 = st.columns(3)
            be, me, fe = c3.selectbox("Batente", OPCOES_ESTADO, key=f"be_{id_chave}"), c4.selectbox("Maçaneta", OPCOES_ESTADO, key=f"me_{id_chave}"), c5.selectbox("Fechadura", OPCOES_ESTADO, key=f"fe_{id_chave}")
            tem_ch = st.checkbox("Tem chave?", key=f"tem_ch_{id_chave}")
            q_ch = st.number_input("Qtd", 0, 10, key=f"qtd_ch_{id_chave}") if tem_ch else 0
            texto_acumulado += f"- Porta de {p_mat} {p_est}, batente {be}, maçaneta {me} e fechadura {fe}{f', acompanhada de {q_ch} {plural(q_ch, 'chave', 'chaves')}' if tem_ch else ', sem chave'}.\n"

        # 4. ILUMINAÇÃO
        if st.checkbox("Iluminação", key=f"inc_ilu_{id_chave}"):
            t_ilu = st.selectbox("Tipo", ["plafon", "spot", "luminária led"], key=f"til_{id_chave}")
            c1, c2, c3 = st.columns(3)
            q_i, e_i, q_l = c1.number_input("Qtd", 1, 20, key=f"qilu_{id_chave}"), c2.selectbox("Estado", OPCOES_ESTADO, key=f"eilu_{id_chave}"), c3.number_input("Lâmp.", 1, 10, key=f"qlamp_{id_chave}")
            f_l = st.radio("Status", ["funcionando", "queimada", "faltante"], key=f"flamp_{id_chave}", horizontal=True)
            det = "de vidro " if t_ilu == "plafon" else f"de {st.selectbox('Mat. Spot', OPCOES_MAT_SPOT, key=f'mspot_{id_chave}')} " if t_ilu == "spot" else ""
            texto_acumulado += f"- {q_i:02} {plural(q_i, t_ilu, t_ilu+'s')} {det}{e_i}, com {q_l:02} {plural(q_l, 'lâmpada', 'lâmpadas')} {f_l}.\n"

        # 5. ELÉTRICA
        if st.checkbox("Elétrica", key=f"inc_ele_{id_chave}"):
            c1, c2, c3 = st.columns(3)
            tom, inter, ee = c1.number_input('Esp. Tomada', 0, 50, key=f't_{id_chave}'), c2.number_input('Interr.', 0, 50, key=f'i_{id_chave}'), c3.selectbox('Est. Geral', OPCOES_ESTADO, key=f'ee_{id_chave}')
            texto_acumulado += f"- {tom:02} {plural(tom, 'espelho tomada', 'espelhos tomadas')} e {inter:02} {plural(inter, 'interruptor', 'interruptores')} {ee}.\n"

        # 6. OBSERVAÇÕES ADICIONAIS (Novo!)
        obs = st.text_area("Notas extras deste cômodo:", key=f"obs_{id_chave}", placeholder="Ex: Mancha de infiltração no canto superior esquerdo.")
        if obs: texto_acumulado += f"- Obs: {obs}\n"

    return f"\n{titulo_secao}\n{texto_acumulado}"

# --- APP ---
st.title("📋 Vistoria Digital")
q_q, q_s = st.columns(2)
num_q, num_s = q_q.number_input("Quartos", 0, 10, 1), q_s.number_input("Suítes", 0, 10, 0)
areas = st.multiselect("Áreas:", ["Sala", "Corredor", "Cozinha", "Banheiro Social", "Área de Serviço"], default=["Sala", "Cozinha"])

relatorio = ""
for area in areas: relatorio += formulario_base(area.lower(), area)
for i in range(num_q): relatorio += formulario_base(f"q{i}", f"Quarto {i+1}")
for i in range(num_s):
    relatorio += formulario_base(f"sq{i}", f"Suíte {i+1}")
    relatorio += formulario_base(f"sb{i}", f"Banheiro Suíte {i+1}")

if relatorio:
    st.header("📄 Relatório Final")
    st.text_area("Preview:", relatorio, height=200)
    html_word = f"<html><head><meta charset='utf-8'></head><body style='font-family:Times New Roman; font-size:12pt;'>{relatorio.replace(chr(10), '<br>')}</body></html>"
    st.download_button("📥 Baixar Word", html_word, "vistoria.doc", "application/msword")
