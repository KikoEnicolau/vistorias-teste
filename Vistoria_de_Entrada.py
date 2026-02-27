import streamlit as st

# Configuração da página com visual de App
st.set_page_config(page_title="Vistoria Pro v11", page_icon="🏠", layout="centered")

# --- CSS CUSTOMIZADO PARA DESIGN DE APP ---
st.markdown("""
    <style>
    /* Fundo e Container */
    .main { background-color: #f0f2f6; }
    .stApp { max-width: 600px; margin: 0 auto; }
    
    /* Estilo dos Cards (Expander) */
    div[data-testid="stExpander"] {
        background-color: white !important;
        border: none !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
        padding: 5px !important;
    }
    
    /* Títulos dos Expanders */
    div[data-testid="stExpander"] p {
        font-weight: 600 !important;
        color: #1E1E1E !important;
        font-size: 1.1rem !important;
    }

    /* Botões */
    .stButton>button {
        width: 100%;
        border-radius: 12px !important;
        height: 3.5rem !important;
        background-image: linear-gradient(to right, #2b5876, #4e4376) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        transition: 0.3s;
    }
    
    /* Inputs */
    .stSelectbox, .stNumberInput {
        margin-bottom: 10px !important;
    }
    
    /* Títulos de Seção */
    h4 {
        color: #4e4376;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE TEXTO (IGUAL À ANTERIOR, APENAS O VISUAL MUDOU) ---
OPCOES_ESTADO = ["em bom estado", "novo", "usado", "com avarias"]
OPCOES_CORES = ["branca", "gelo", "cinza", "bege", "preta", "marrom", "amadeirada", "off-white", "natural"]
OPCOES_PISO_MAT = ["frio", "cerâmico", "porcelanato", "laminado", "vinílico", "ardósia", "taco/mad."]

def plural(qtd, singular, plural): return singular if qtd <= 1 else plural

def gerar_formulario(id_chave, nome_exibicao):
    with st.expander(f"📍 {nome_exibicao.upper()}", expanded=False):
        texto = ""
        
        # --- SEÇÃO 1: ESTRUTURA ---
        st.markdown("#### 🏗️ Estrutura")
        c1, c2 = st.columns(2)
        p_mat = c1.selectbox("Piso", OPCOES_PISO_MAT, key=f"p_mat_{id_chave}")
        p_est = c2.selectbox("Estado", OPCOES_ESTADO, key=f"p_est_{id_chave}")
        p_cor = st.selectbox("Cor do Piso", OPCOES_CORES, key=f"p_cor_{id_chave}")
        texto += f"- Piso {p_mat} na cor {p_cor}, {p_est}.\n"

        if st.checkbox("Incluir Rodapé", key=f"check_r_{id_chave}"):
            r1, r2 = st.columns(2)
            r_mat = r1.selectbox("Material Rodapé", OPCOES_PISO_MAT, key=f"r_mat_{id_chave}")
            r_est = r2.selectbox("Estado Rodapé", OPCOES_ESTADO, key=f"r_est_{id_chave}")
            texto += f"- Rodapé em {r_mat} na cor {p_cor}, {r_est}.\n"

        # --- SEÇÃO 2: ACABAMENTO ---
        st.markdown("#### 🎨 Acabamento")
        par_cor = st.selectbox("Cor das Paredes", OPCOES_CORES, key=f"par_cor_{id_chave}")
        par_est = st.selectbox("Estado Paredes", OPCOES_ESTADO, key=f"par_est_{id_chave}")
        texto += f"- Paredes na cor {par_cor}, {par_est}.\n"

        # --- SEÇÃO 3: PORTA ---
        st.markdown("#### 🚪 Porta")
        c3, c4 = st.columns(2)
        po_mat = c3.selectbox("Material Porta", ["madeira", "alumínio", "ferro"], key=f"po_mat_{id_chave}")
        po_est = c4.selectbox("Estado Porta", OPCOES_ESTADO, key=f"po_est_{id_chave}")
        
        c5, c6 = st.columns(2)
        mac = c5.selectbox("Maçaneta", OPCOES_ESTADO, key=f"mac_{id_chave}")
        fec = c6.selectbox("Fechadura", OPCOES_ESTADO, key=f"fec_{id_chave}")
        
        tem_ch = st.checkbox("Possui Chaves?", key=f"ch_{id_chave}")
        qtd_ch = st.number_input("Qtd Chaves", 0, 5, key=f"qch_{id_chave}") if tem_ch else 0
        txt_ch = f", acompanhada de {qtd_ch} {plural(qtd_ch, 'chave', 'chaves')}" if tem_ch else ", sem chave"
        
        texto += f"- Porta de {po_mat} {po_est}, maçaneta {mac} e fechadura {fec}{txt_ch}.\n"

        # --- SEÇÃO 4: ELÉTRICA E LUZ ---
        st.markdown("#### 💡 Elétrica e Luz")
        e1, e2 = st.columns(2)
        tom = e1.number_input("Espelhos Tomada", 0, 20, key=f"tom_{id_chave}")
        int_ = e2.number_input("Interruptores", 0, 20, key=f"int_{id_chave}")
        texto += f"- {tom:02} {plural(tom, 'espelho tomada', 'espelhos tomadas')} e {int_:02} {plural(int_, 'interruptor', 'interruptores')} em bom estado.\n"

        obs = st.text_input("Observações Adicionais", key=f"obs_{id_chave}", placeholder="Ex: Risco atrás da porta")
        if obs: texto += f"- Obs: {obs}\n"
        
    return texto

# --- INTERFACE PRINCIPAL ---
st.title("Vistoria Pro")
st.markdown("Preencha as informações dos cômodos abaixo.")

# Seleção de Cômodos (Mais visual)
col_a, col_b = st.columns(2)
quartos = col_a.number_input("Nº Quartos", 0, 5, 1)
suites = col_b.number_input("Nº Suítes", 0, 5, 0)

areas_comuns = st.multiselect("Selecione as áreas:", 
                              ["Sala", "Cozinha", "Banheiro Social", "Área de Serviço", "Corredor"],
                              default=["Sala", "Cozinha"])

relatorio_completo = ""

# Barra de Progresso Simbólica
st.progress(0.5) 

# Geração dos Cards
for area in areas_comuns:
    relatorio_completo += f"\n{area.upper()}\n"
    relatorio_completo += gerar_formulario(area.lower(), area)

for i in range(quartos):
    relatorio_completo += f"\nQUARTO {i+1}\n"
    relatorio_completo += gerar_formulario(f"q{i}", f"Quarto {i+1}")

for i in range(suites):
    relatorio_completo += f"\nSUÍTE {i+1}\n"
    relatorio_completo += gerar_formulario(f"s{i}", f"Suíte {i+1}")

# --- RODAPÉ DE FINALIZAÇÃO ---
if relatorio_completo:
    st.markdown("---")
    st.subheader("🏁 Finalizar Vistoria")
    
    with st.expander("👁️ Visualizar Texto"):
        st.text(relatorio_completo)
    
    # Botão de Download com Design
    html_word = f"<html><head><meta charset='utf-8'></head><body style='font-family:Times New Roman; font-size:12pt;'>{relatorio_completo.replace(chr(10), '<br>')}</body></html>"
    
    st.download_button(
        label="📥 GERAR E BAIXAR RELATÓRIO",
        data=html_word,
        file_name="vistoria_final.doc",
        mime="application/msword"
    )
