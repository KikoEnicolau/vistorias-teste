import streamlit as st

# Configuração da Página
st.set_page_config(page_title="Vistoria Pro", page_icon="📋", layout="centered")

# --- CSS PARA ESTILO BASE44 / VISTORIA PRO ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    header {visibility: hidden;}
    
    /* Header Principal */
    .main-header {
        background-color: #1a202c;
        padding: 15px;
        color: white;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        border-radius: 0 0 10px 10px;
        margin-bottom: 20px;
    }

    /* Estilo dos Cards */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f1f5f9;
        border-radius: 8px;
        padding: 0 20px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: white !important;
    }

    /* Botões */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.5rem;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
    }
    </style>
    <div class="main-header">📋 Vistoria Pro</div>
    """, unsafe_allow_html=True)

# --- CONTROLE DE ESTADO (ETAPAS) ---
if 'etapa' not in st.session_state:
    st.session_state.etapa = 1
if 'dados_imovel' not in st.session_state:
    st.session_state.dados_imovel = {}
if 'comodos_selecionados' not in st.session_state:
    st.session_state.comodos_selecionados = []

# --- ETAPA 1: INFORMAÇÕES BÁSICAS ---
if st.session_state.etapa == 1:
    with st.container():
        st.subheader("📄 Nova Vistoria")
        with st.expander("📍 Endereço do Imóvel", expanded=True):
            endereco = st.text_input("Ex: Rua das Flores, 123", placeholder="Digite o endereço...")
            c1, c2 = st.columns(2)
            data = c1.date_input("Data")
            tipo = c2.selectbox("Tipo", ["Entrada", "Saída", "Conferência"])
            
            if st.button("Continuar"):
                if endereco:
                    st.session_state.dados_imovel = {"endereco": endereco, "data": data, "tipo": tipo}
                    st.session_state.etapa = 2
                    st.rerun()
                else:
                    st.error("Por favor, preencha o endereço.")

# --- ETAPA 2: CONFIGURAÇÃO DO IMÓVEL ---
elif st.session_state.etapa == 2:
    st.subheader("🏠 Configuração do Imóvel")
    st.write("Selecione os cômodos:")
    
    opcoes = {
        "🛋️ Sala": "Sala",
        "📑 Corredor": "Corredor",
        "🍳 Cozinha": "Cozinha",
        "🚿 Banheiro Social": "Banheiro Social",
        "🧺 Área de Serviço": "Área de Serviço",
        "🚗 Garagem": "Garagem"
    }
    
    selecionados = []
    for label, nome in opcoes.items():
        if st.checkbox(label):
            selecionados.append(nome)
    
    c1, c2 = st.columns(2)
    quartos = c1.number_input("Quartos", 0, 10, 1)
    suites = c2.number_input("Suítes", 0, 10, 0)
    
    if st.button(f"Continuar ({len(selecionados) + quartos + (suites*2)} cômodos)"):
        # Monta a lista final de abas
        lista_final = selecionados
        for i in range(quartos): lista_final.append(f"Quarto {i+1}")
        for i in range(suites): 
            lista_final.append(f"Suíte {i+1}")
            lista_final.append(f"Banheiro Suíte {i+1}")
        
        st.session_state.comodos_selecionados = lista_final
        st.session_state.etapa = 3
        st.rerun()

# --- ETAPA 3: VISTORIA (SISTEMA DE ABAS IGUAL À FOTO) ---
elif st.session_state.etapa == 3:
    st.info(f"📍 {st.session_state.dados_imovel['endereco']}")
    
    # Cria as Abas no topo (Navegação horizontal)
    tabs = st.tabs(st.session_state.comodos_selecionados)
    
    relatorio_final = f"VISTORIA: {st.session_state.dados_imovel['endereco']}\n"
    relatorio_final += f"DATA: {st.session_state.dados_imovel['data']} | TIPO: {st.session_state.dados_imovel['tipo']}\n\n"

    OPCOES_ESTADO = ["Selecione", "Em bom estado", "Novo", "Com avarias"]

    # Preenche cada Aba
    for i, tab in enumerate(tabs):
        nome_comodo = st.session_state.comodos_selecionados[i]
        with tab:
            st.write(f"### {nome_comodo}")
            
            # Sub-seções expansíveis (Piso, Rodapé, etc.) como na sua foto 4
            with st.expander("Piso", expanded=True):
                c1, c2 = st.columns(2)
                mat = c1.selectbox("Material", ["Porcelanato", "Cerâmico", "Laminado"], key=f"mat_{i}")
                cor = c2.selectbox("Cor", ["Branca", "Bege", "Cinza"], key=f"cor_{i}")
                est = st.selectbox("Estado", OPCOES_ESTADO, key=f"est_{i}")
                st.write("📷 **Fotos**")
                st.file_uploader("Upload", type=['jpg', 'png'], key=f"foto_{i}", label_visibility="collapsed")

            with st.expander("Paredes"):
                st.selectbox("Estado Pintura", OPCOES_ESTADO, key=f"par_{i}")
            
            with st.expander("Porta"):
                st.selectbox("Estado Geral", OPCOES_ESTADO, key=f"por_{i}")

            with st.expander("Observações"):
                st.text_area("Notas extras", key=f"obs_{i}")

    st.markdown("---")
    if st.button("💾 Gerar Relatório Final"):
        st.success("Relatório gerado com sucesso!")
        # Aqui você pode adicionar a lógica de download do Word que já tínhamos
