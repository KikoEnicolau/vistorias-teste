import streamlit as st

# Configuração da página
st.set_page_config(page_title="Vistoria Pro", page_icon="📋", layout="centered")

# --- DESIGN INSPIRADO NO BASE44 (CSS) ---
st.markdown("""
    <style>
    /* Fundo geral mais claro e moderno */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Barra Superior Fixa */
    .header {
        background-color: #1e293b;
        padding: 15px;
        color: white;
        text-align: center;
        font-weight: bold;
        border-radius: 0 0 15px 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }

    /* Estilo dos Cartões de Cômodos */
    div[data-testid="stExpander"] {
        background-color: white !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08) !important;
        margin-bottom: 20px !important;
        padding: 10px;
    }

    /* Títulos dos Cards */
    div[data-testid="stExpander"] p {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #334155 !important;
    }

    /* Botão de Finalização Estilo App */
    .stButton>button {
        width: 100%;
        background-color: #2563eb !important;
        color: white !important;
        border-radius: 10px !important;
        height: 3.5rem !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
    }

    /* Ajuste de Margens e Padding */
    .block-container {
        padding-top: 1rem !important;
    }
    </style>
    
    <div class="header">📋 SISTEMA DE VISTORIA PROFISSIONAL</div>
    """, unsafe_allow_html=True)

# --- LISTAS E FUNÇÕES ---
OPCOES_ESTADO = ["em bom estado", "novo", "usado", "com avarias"]
OPCOES_PISO = ["porcelanato", "cerâmico", "laminado", "vinílico", "ardósia"]

def plural(qtd, singular, plural): return singular if qtd <= 1 else plural

def criar_card_vistoria(id_chave, nome):
    with st.expander(f"📍 {nome}", expanded=False):
        st.markdown(f"**Detalhes de {nome}**")
        
        # Grid para otimizar espaço
        col1, col2 = st.columns(2)
        p_mat = col1.selectbox("Piso", OPCOES_PISO, key=f"pm_{id_chave}")
        p_est = col2.selectbox("Estado", OPCOES_ESTADO, key=f"pe_{id_chave}")
        
        # Porta e Acessórios
        st.write("---")
        st.caption("Aberturas e Ferragens")
        c3, c4 = st.columns(2)
        po_est = c3.selectbox("Porta", OPCOES_ESTADO, key=f"poe_{id_chave}")
        ja_est = c4.selectbox("Janela", OPCOES_ESTADO, key=f"jae_{id_chave}")
        
        # Iluminação e Elétrica
        st.write("---")
        st.caption("Elétrica e Iluminação")
        c5, c6 = st.columns(2)
        tom = c5.number_input("Tomadas", 0, 30, key=f"t_{id_chave}")
        ilum = c6.selectbox("Iluminação", ["plafon", "spot", "painel led"], key=f"il_{id_chave}")
        
        obs = st.text_area("Observações Específicas", key=f"obs_{id_chave}", placeholder="Ex: Risco no canto da parede...")
        
        # Montagem do Texto
        texto = f"\n{nome.upper()}\n"
        texto += f"- Piso {p_mat}, {p_est}.\n"
        texto += f"- Porta {po_est} e janela {ja_est}.\n"
        texto += f"- {tom:02} {plural(tom, 'espelho tomada', 'espelhos tomadas')} em bom estado.\n"
        texto += f"- Iluminação tipo {ilum} funcionando.\n"
        if obs: texto += f"- Obs: {obs}\n"
        return texto

# --- CORPO DO APP ---
col_q, col_s = st.columns(2)
nq = col_q.number_input("Quartos", 0, 5, 1)
ns = col_s.number_input("Suítes", 0, 5, 0)

areas = st.multiselect("Áreas para Vistoria", 
                       ["Sala", "Cozinha", "Banheiro Social", "Sacada", "Área de Serviço"],
                       default=["Sala", "Cozinha"])

relatorio = ""

for area in areas:
    relatorio += criar_card_vistoria(area.lower(), area)

for i in range(nq):
    relatorio += criar_card_vistoria(f"q{i}", f"Quarto {i+1}")

for i in range(ns):
    relatorio += criar_card_vistoria(f"s{i}", f"Suíte {i+1}")
    relatorio += criar_card_vistoria(f"bs{i}", f"Banheiro Suíte {i+1}")

# --- FINALIZAÇÃO ---
if relatorio:
    st.markdown("### 📄 Relatório Final")
    st.text_area("Prévia:", relatorio, height=150)
    
    html = f"<html><head><meta charset='utf-8'></head><body style='font-family:Times New Roman; font-size:12pt;'>{relatorio.replace(chr(10), '<br>')}</body></html>"
    st.download_button("📥 BAIXAR VISTORIA PRONTA", html, "vistoria.doc", "application/msword")
