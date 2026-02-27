import streamlit as st

# Configuração para visual de Aplicativo Profissional
st.set_page_config(page_title="Vistoria Pro v12", page_icon="🏠", layout="centered")

# --- CSS AVANÇADO PARA LAYOUT DE APP ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    [data-testid="stExpander"] {
        background-color: white !important;
        border-radius: 15px !important;
        border: 1px solid #e1e4e8 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        margin-bottom: 12px !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
        font-weight: bold;
    }
    h4 {
        color: #1a5e20;
        font-size: 0.85rem !important;
        border-bottom: 1px solid #eee;
        padding-bottom: 5px;
        margin-top: 15px !important;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- OPÇÕES ---
OPCOES_ESTADO = ["em bom estado", "novo", "usado", "com avarias"]
OPCOES_CORES = ["branca", "gelo", "cinza", "bege", "preta", "marrom", "amadeirada", "off-white", "natural"]
OPCOES_PISO_MAT = ["frio", "cerâmico", "porcelanato", "laminado", "vinílico", "ardósia", "taco/mad."]
OPCOES_RODAPE_MAT = OPCOES_PISO_MAT + ["madeira/mdf", "poliuretano", "pvc", "poliestireno"]

def plural(qtd, singular, plural): return singular if qtd <= 1 else plural

def gerar_formulario(id_chave, nome_exibicao):
    with st.expander(f"📍 {nome_exibicao.upper()}", expanded=False):
        texto = ""
        
        # 1. PISO E RODAPÉ
        st.markdown("#### 🏗️ Piso e Rodapé")
        c1, c2 = st.columns(2)
        p_mat = c1.selectbox("Material Piso", OPCOES_PISO_MAT, key=f"p_mat_{id_chave}")
        p_est = c2.selectbox("Estado Piso", OPCOES_ESTADO, key=f"p_est_{id_chave}")
        p_cor = st.selectbox("Cor do Piso", OPCOES_CORES, key=f"p_cor_{id_chave}")
        texto += f"- Piso {p_mat} na cor {p_cor}, {p_est}.\n"

        if st.checkbox("Incluir Rodapé", key=f"check_r_{id_chave}"):
            r1, r2 = st.columns(2)
            r_mat = r1.selectbox("Mat. Rodapé", OPCOES_RODAPE_MAT, key=f"r_mat_{id_chave}")
            r_est = r2.selectbox("Est. Rodapé", OPCOES_ESTADO, key=f"r_est_{id_chave}")
            texto += f"- Rodapé em {r_mat} na cor {p_cor}, {r_est}.\n"

        # 2. PAREDES E TETO
        st.markdown("#### 🎨 Paredes e Teto")
        tipo_p = st.radio("Tipo de Parede", ["Alvenaria", "Azulejo"], key=f"tp_{id_chave}", horizontal=True)
        c3, c4 = st.columns(2)
        pa_cor = c3.selectbox("Cor Parede", OPCOES_CORES, key=f"pa_c_{id_chave}") if tipo_p == "Alvenaria" else "revestimento"
        pa_est = c4.selectbox("Estado Parede", OPCOES_ESTADO, key=f"pa_e_{id_chave}")
        texto += f"- Paredes {'na cor ' + pa_cor if tipo_p == 'Alvenaria' else 'com azulejos'}, {pa_est}.\n"
        
        c5, c6 = st.columns(2)
        t_cor = c5.selectbox("Cor Teto", OPCOES_CORES, key=f"t_c_{id_chave}")
        t_est = c6.selectbox("Estado Teto", OPCOES_ESTADO, key=f"t_e_{id_chave}")
        gesso = st.checkbox("Moldura de gesso?", key=f"gs_{id_chave}")
        texto += f"- Teto na cor {t_cor}, {t_est}{' com moldura de gesso' if gesso else ' sem moldura'}.\n"

        # 3. PORTA E JANELA
        st.markdown("#### 🚪 Aberturas")
        if st.checkbox("Incluir Porta", key=f"inc_po_{id_chave}", value=True):
            c7, c8 = st.columns(2)
            po_mat = c7.selectbox("Material Porta", ["madeira", "alumínio", "ferro"], key=f"po_m_{id_chave}")
            po_est = c8.selectbox("Estado Porta", OPCOES_ESTADO, key=f"po_e_{id_chave}")
            c9, c10, c11 = st.columns(3)
            be, me, fe = c9.selectbox("Batente", OPCOES_ESTADO, key=f"be_{id_chave}"), c10.selectbox("Maçaneta", OPCOES_ESTADO, key=f"me_{id_chave}"), c11.selectbox("Fechadura", OPCOES_ESTADO, key=f"fe_{id_chave}")
            tem_ch = st.checkbox("Tem chave?", key=f"ch_{id_chave}")
            q_ch = st.number_input("Qtd Chaves", 0, 10, key=f"qch_{id_chave}") if tem_ch else 0
            texto += f"- Porta de {po_mat} {po_est}, batente {be}, maçaneta {me} e fechadura {fe}{', acompanhada de ' + str(q_ch) + ' ' + plural(q_ch, 'chave', 'chaves') if tem_ch else ', sem chave'}.\n"

        if st.checkbox("Incluir Janela", key=f"inc_ja_{id_chave}"):
            cj1, cj2 = st.columns(2)
            jm, je = cj1.selectbox("Material Janela", ["alumínio", "ferro"], key=f"jm_{id_chave}"), cj2.selectbox("Estado Janela", OPCOES_ESTADO, key=f"je_{id_chave}")
            texto += f"- Janela de {jm} {je} em bom estado.\n"

        # 4. ILUMINAÇÃO
        st.markdown("#### 💡 Iluminação")
        if st.checkbox("Incluir Iluminação", key=f"inc_il_{id_chave}"):
            til = st.selectbox("Tipo", ["plafon", "spot", "luminária led"], key=f"til_{id_chave}")
            ci1, ci2, ci3 = st.columns(3)
            qi, ei, ql = ci1.number_input("Qtd Itens", 1, 20, key=f"qi_{id_chave}"), ci2.selectbox("Estado", OPCOES_ESTADO, key=f"ei_{id_chave}"), ci3.number_input("Lâmpadas", 1, 10, key=f"ql_{id_chave}")
            fl = st.radio("Status Lâmpada", ["funcionando", "queimada", "faltante"], key=f"fl_{id_chave}", horizontal=True)
            det = "de vidro " if til == "plafon" else ""
            texto += f"- {qi:02} {plural(qi, til, til+'s')} {det}{ei}, com {ql:02} {plural(ql, 'lâmpada', 'lâmpadas')} {fl}.\n"

        # 5. ELÉTRICA E RALO
        st.markdown("#### ⚡ Elétrica e Outros")
        ce1, ce2 = st.columns(2)
        tom = ce1.number_input("Espelhos Tomada", 0, 50, key=f"t_{id_chave}")
        int_ = ce2.number_input("Interruptores", 0, 50, key=f"i_{id_chave}")
        est_e = st.selectbox("Estado Elétrica", OPCOES_ESTADO, key=f"ee_{id_chave}")
        texto += f"- {tom:02} {plural(tom, 'espelho tomada', 'espelhos tomadas')} e {int_:02} {plural(int_, 'interruptor', 'interruptores')} {est_e}.\n"
        
        if st.checkbox("Incluir Ralo", key=f"ra_{id_chave}"):
            rq = st.number_input("Qtd Ralos", 1, 10, key=f"rq_{id_chave}")
            texto += f"- {rq:02} {plural(rq, 'unidade de ralo', 'unidades de ralo')} em bom estado.\n"

        obs = st.text_input("Observações", key=f"obs_{id_chave}")
        if obs: texto += f"- Obs: {obs}\n"
        
    return texto

# --- APP ---
st.title("🏠 Vistoria Profissional")

# Configuração inicial
c_q, c_s = st.columns(2)
n_q = c_q.number_input("Quartos", 0, 10, 1)
n_s = c_s.number_input("Suítes", 0, 10, 0)
areas = st.multiselect("Áreas comuns:", ["Sala", "Cozinha", "Banheiro Social", "Área de Serviço", "Corredor"], default=["Sala", "Cozinha"])

relatorio = ""
for a in areas: relatorio += f"\n{a.upper()}\n" + gerar_formulario(a.lower(), a)
for i in range(n_q): relatorio += f"\nQUARTO {i+1}\n" + gerar_formulario(f"q{i}", f"Quarto {i+1}")
for i in range(n_s):
    relatorio += f"\nSUÍTE {i+1}\n" + gerar_formulario(f"s{i}", f"Suíte {i+1}")
    relatorio += f"\nBANHEIRO SUÍTE {i+1}\n" + gerar_formulario(f"bs{i}", f"Banheiro Suíte {i+1}")

if relatorio:
    st.markdown("---")
    st.subheader("📄 Relatório Final")
    st.text_area("Texto gerado:", relatorio, height=200)
    
    html = f"<html><head><meta charset='utf-8'></head><body style='font-family:Times New Roman; font-size:12pt;'>{relatorio.replace(chr(10), '<br>')}</body></html>"
    st.download_button("📥 BAIXAR VISTORIA EM WORD", html, "vistoria.doc", "application/msword")
