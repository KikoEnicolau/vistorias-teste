import streamlit as st

# Configuração da página para parecer um aplicativo nativo
st.set_page_config(page_title="Vistoria Pro", page_icon="📋", layout="centered", initial_sidebar_state="collapsed")

# --- CSS AVANÇADO PARA CLONAR O VISUAL BASE44 ---
st.markdown("""
    <style>
    /* FUNDO GERAL LIMPO */
    .stApp {
        background-color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* REMOVE A BARRA PADRÃO DO STREAMLIT */
    header {visibility: hidden;}
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}

    /* HEADER FIXO ESTILO APP */
    .header {
        background-color: #1e293b;
        padding: 20px 15px;
        color: white;
        text-align: center;
        font-weight: 700;
        font-size: 1.3rem;
        border-radius: 0 0 15px 15px;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 999;
    }
    
    /* CARTÕES FLUTUANTES (EXPANDERS) */
    div[data-testid="stExpander"] {
        background-color: white !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
        padding: 5px;
    }

    /* TÍTULOS DOS CARTÕES */
    div[data-testid="stExpander"] p {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #1a202c !important;
    }

    /* DIVISORES SUTIS */
    div[data-testid="stExpander"] hr {
        border-top: 1px solid #edf2f7 !important;
        margin: 10px 0 !important;
    }

    /* CAPTIONS E LEGENDAS */
    div[data-testid="stExpander"] span {
        font-size: 0.8rem !important;
        color: #718096 !important;
    }

    /* BOTÃO FINAL GRANDE E AZUL */
    .stButton>button {
        width: 100%;
        border-radius: 12px !important;
        height: 3.5rem !important;
        background-color: #2563eb !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: 0.2s;
        box-shadow: 0 10px 15px rgba(37, 99, 235, 0.2);
    }
    .stButton>button:hover {
        background-color: #1d4ed8 !important;
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.3);
    }

    /* TÍTULOS DE SEÇÃO */
    h3 {
        color: #1a202c;
        font-size: 1.3rem !important;
        margin-top: 25px !important;
        margin-bottom: 10px !important;
    }
    </style>
    
    <div class="header">📋 SISTEMA DE VISTORIA PROFISSIONAL</div>
    """, unsafe_allow_html=True)

# --- OPÇÕES TÉCNICAS (PADRONIZADO) ---
OPCOES_ESTADO = ["em bom estado", "novo", "usado", "com avarias"]
OPCOES_PISO = ["porcelanato", "cerâmico", "laminado", "vinílico", "ardósia", "taco"]
OPCOES_ILUM = ["plafon", "spot", "painel led"]
OPCOES_CORES = ["branca", "gelo", "cinza", "bege", "preta", "marrom", "natural"]

def plural(qtd, singular, plural): return singular if qtd <= 1 else plural

# --- FUNÇÃO PRINCIPAL: GERAR CARTÃO DE CÔMODO ---
def criar_card_vistoria(id_chave, nome):
    # O expander externo agora é o "cartão" do cômodo
    with st.expander(f"📍 {nome.upper()}", expanded=False):
        
        texto = f"\n{nome.upper()}\n"
        
        # --- CARDS INTERNOS (ESTILO BASE44) ---
        
        # 1. PISO E RODAPÉ (Tudo no mesmo bloco compactado)
        st.caption("🏗️ Piso e Acabamento")
        col_p1, col_p2 = st.columns(2)
        p_mat = col_p1.selectbox("Material Piso", OPCOES_PISO, key=f"pm_{id_chave}")
        p_est = col_p2.selectbox("Estado", OPCOES_ESTADO, key=f"pe_{id_chave}")
        p_cor = st.selectbox("Cor do Piso", OPCOES_CORES, key=f"pc_{id_chave}")
        
        texto += f"- Piso {p_mat} na cor {p_cor}, {p_est}.\n"
        
        # Checagem de Rodapé em linha única
        if st.checkbox("Incluir Rodapé?", key=f"ck_r_{id_chave}"):
            texto += f"- Rodapé do mesmo material e cor, bom estado.\n"

        st.markdown("---")
        
        # 2. PAREDES E TETO (Convertido em 2 colunas)
        st.caption("🎨 Acabamento e Cor")
        col_pt1, col_pt2 = st.columns(2)
        pa_cor = col_pt1.selectbox("Cor Parede", OPCOES_CORES, key=f"pac_{id_chave}")
        pa_est = col_pt2.selectbox("Estado Parede", OPCOES_ESTADO, key=f"pae_{id_chave}")
        te_est = st.selectbox("Estado Teto", OPCOES_ESTADO, key=f"tee_{id_chave}")
        
        gesso = st.checkbox("Moldura de gesso?", key=f"gs_{id_chave}")
        texto += f"- Paredes na cor {pa_cor}, {pa_est}. Teto em bom estado{' com moldura de gesso' if gesso else ' sem moldura'}.\n"

        st.markdown("---")
        
        # 3. PORTA E JANELA (Compactado em 2 colunas principais)
        st.caption("🚪 Aberturas")
        col_pj1, col_pj2 = st.columns(2)
        po_est = col_pj1.selectbox("Porta", OPCOES_ESTADO, key=f"poe_{id_chave}")
        ja_est = col_pj2.selectbox("Janela", OPCOES_ESTADO, key=f"jae_{id_chave}")
        
        # Lógica avançada de porta trazida de volta e compactada
        col_pj3, col_pj4 = st.columns(2)
        bat_est = col_pj3.selectbox("Batente/Alizar", OPCOES_ESTADO, key=f"be_{id_chave}")
        fec_est = col_pj4.selectbox("Maçaneta/Fechad.", OPCOES_ESTADO, key=f"fe_{id_chave}")
        
        tem_ch = st.checkbox("Possui Chaves?", key=f"ch_{id_chave}")
        qtd_ch = st.number_input("Qtd", 0, 5, key=f"qch_{id_chave}") if tem_ch else 0
        txt_ch = f", acompanhada de {qtd_ch} {plural(qtd_ch, 'chave', 'chaves')}" if tem_ch else ", sem chave"
        
        texto += f"- Porta madeira {po_est}, batente {bat_est}, maçaneta {fec_est}{txt_ch}.\n"
        texto += f"- Janela {ja_est}.\n"

        st.markdown("---")
        
        # 4. ELÉTRICA E ILUMINAÇÃO (Organizado em grade sutil)
        st.caption("💡 Elétrica e Luz")
        col_ei1, col_ei2 = st.columns(2)
        tom = col_ei1.number_input("Tomadas", 0, 50, key=f"t_{id_chave}")
        il_tipo = col_ei2.selectbox("Tipo Ilum.", OPCOES_ILUM, key=f"ilt_{id_chave}")
        il_lamp = st.selectbox("Lâmpadas?", ["funcionando", "faltantes", "queimadas"], key=f"ill_{id_chave}")
        
        texto += f"- {tom:02} {plural(tom, 'espelho tomada', 'espelhos tomadas')} em bom estado.\n"
        texto += f"- Iluminação {il_tipo} {il_lamp}.\n"

        st.markdown("---")
        
        # 5. OBSERVAÇÕES E RALO
        st.caption("⚡ Outros")
        obs = st.text_input("Observações Técnicas", key=f"obs_{id_chave}")
        ralo = st.checkbox("Incluir Ralo?", key=f"rl_{id_chave}")
        
        if obs: texto += f"- Obs: {obs}\n"
        if ralo: texto += f"- Ralo inox bom estado.\n"
        
        return texto

# --- CONFIGURAÇÃO INICIAL (LAYOUT COMPACTO) ---
st.write("### 🏠 Novo Relatório")
c_q, c_s = st.columns(2)
nq = c_q.number_input("Nº Quartos", 0, 5, 1)
ns = c_s.number_input("Nº Suítes", 0, 5, 0)

areas = st.multiselect("Áreas para Vistoria:", 
                       ["Sala", "Cozinha", "Banheiro Social", "Sacada/Varanda", "Área de Serviço", "Corredor"],
                       default=["Sala", "Cozinha"])

relatorio = ""

# --- GERAÇÃO DOS CÔMODOS ---
# Fundo cinza para os cards brancos flutuarem
for area in areas: relatorio += criar_card_vistoria(area.lower(), area)
for i in range(nq): relatorio += criar_card_vistoria(f"q{i}", f"Quarto {i+1}")
for i in range(ns):
    relatorio += criar_card_vistoria(f"s{i}", f"Suíte {i+1}")
    relatorio += criar_card_vistoria(f"bs{i}", f"Banheiro Suíte {i+1}")

# --- FINALIZAÇÃO ---
if relatorio:
    st.markdown("---")
    st.write("### 🏁 Finalizar Vistoria")
    
    with st.expander("👁️ Pré-visualizar Relatório Completo", expanded=False):
        st.text_area("Texto gerado:", relatorio, height=200)
    
    # Formatação Word (Mantido)
    html_doc = f"<html><head><meta charset='utf-8'></head><body style='font-family:Times New Roman; font-size:12pt;'>{relatorio.replace(chr(10), '<br>')}</body></html>"
    
    st.download_button(
        label="📥 BAIXAR RELATÓRIO PRONTO (WORD)",
        data=html_doc,
        file_name="vistoria_final.doc",
        mime="application/msword"
    )
