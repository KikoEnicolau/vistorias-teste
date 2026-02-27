import streamlit as st
from docx import Document
from docx.shared import Inches
import io

# Configuração da Página
st.set_page_config(page_title="Vistoria Pro", page_icon="📋", layout="centered")

# --- CSS (MANTIDO DO ANTERIOR) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    header {visibility: hidden;}
    .main-header {
        background-color: #1a202c; padding: 15px; color: white;
        text-align: center; font-size: 1.5rem; font-weight: bold;
        border-radius: 0 0 10px 10px; margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #f1f5f9; border-radius: 8px; }
    .stTabs [aria-selected="true"] { background-color: #2563eb !important; color: white !important; }
    </style>
    <div class="main-header">📋 Vistoria Pro</div>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DA MEMÓRIA (SALVAMENTO AUTOMÁTICO) ---
if 'etapa' not in st.session_state: st.session_state.etapa = 1
if 'dados_vistoria' not in st.session_state: st.session_state.dados_vistoria = {}
if 'fotos' not in st.session_state: st.session_state.fotos = {}

# --- ETAPA 1: INFORMAÇÕES BÁSICAS ---
if st.session_state.etapa == 1:
    st.subheader("📄 Nova Vistoria")
    with st.expander("📍 Identificação", expanded=True):
        end = st.text_input("Endereço", key="input_end")
        c1, c2 = st.columns(2)
        data = c1.date_input("Data")
        tipo = c2.selectbox("Tipo", ["Entrada", "Saída"])
        
        if st.button("Continuar"):
            if end:
                st.session_state.info_geral = {"end": end, "data": data, "tipo": tipo}
                st.session_state.etapa = 2
                st.rerun()

# --- ETAPA 2: ESCOLHA DE CÔMODOS ---
elif st.session_state.etapa == 2:
    st.subheader("🏠 Configuração")
    opcoes = ["Sala", "Cozinha", "Banheiro Social", "Área de Serviço", "Corredor", "Garagem"]
    selecionados = []
    for item in opcoes:
        if st.checkbox(item, key=f"chk_{item}"): selecionados.append(item)
    
    c1, c2 = st.columns(2)
    q = c1.number_input("Quartos", 0, 5, 1)
    s = c2.number_input("Suítes", 0, 5, 0)
    
    if st.button("Iniciar Vistoria"):
        lista = selecionados + [f"Quarto {i+1}" for i in range(q)]
        for i in range(s):
            lista.append(f"Suíte {i+1}")
            lista.append(f"Banheiro Suíte {i+1}")
        st.session_state.comodos = lista
        st.session_state.etapa = 3
        st.rerun()

# --- ETAPA 3: PREENCHIMENTO E SALVAMENTO ---
elif st.session_state.etapa == 3:
    st.caption(f"📍 {st.session_state.info_geral['end']}")
    tabs = st.tabs(st.session_state.comodos)
    
    for i, nome_comodo in enumerate(st.session_state.comodos):
        with tabs[i]:
            st.write(f"### {nome_comodo}")
            
            # Criamos chaves únicas para salvar cada campo na memória
            key_base = f"{nome_comodo}_{i}"
            
            # Piso
            with st.expander("Piso", expanded=True):
                # O parâmetro 'key' abaixo garante que o dado fique salvo no session_state automaticamente
                st.selectbox("Material", ["Porcelanato", "Laminado", "Cerâmico"], key=f"piso_mat_{key_base}")
                st.selectbox("Estado", ["Bom", "Novo", "Avarias"], key=f"piso_est_{key_base}")
                
                foto = st.file_uploader("📷 Foto do Piso", type=['jpg', 'png'], key=f"foto_piso_{key_base}")
                if foto: st.session_state.fotos[f"foto_piso_{key_base}"] = foto

            # Paredes
            with st.expander("Paredes"):
                st.selectbox("Pintura", ["Fosca", "Acetinada"], key=f"par_pin_{key_base}")
                st.selectbox("Estado", ["Bom", "Novo", "Riscado"], key=f"par_est_{key_base}")

            # Observações
            st.text_area("Notas extras", key=f"obs_{key_base}")

    st.markdown("---")
    
    # --- GERAÇÃO DO ARQUIVO WORD ---
    if st.button("📊 GERAR RELATÓRIO FINAL"):
        doc = Document()
        doc.add_heading('Relatório de Vistoria', 0)
        doc.add_paragraph(f"Imóvel: {st.session_state.info_geral['end']}")
        doc.add_paragraph(f"Data: {st.session_state.info_geral['data']} | Tipo: {st.session_state.info_geral['tipo']}")

        for i, nome in enumerate(st.session_state.comodos):
            key_base = f"{nome}_{i}"
            doc.add_heading(nome, level=1)
            
            # Puxando dados da memória do Streamlit
            mat = st.session_state.get(f"piso_mat_{key_base}")
            est = st.session_state.get(f"piso_est_{key_base}")
            doc.add_paragraph(f"Piso: Material {mat} em estado {est}.")
            
            obs = st.session_state.get(f"obs_{key_base}")
            if obs: doc.add_paragraph(f"Observações: {obs}")

            # Adicionando a Foto se existir
            foto_key = f"foto_piso_{key_base}"
            if foto_key in st.session_state.fotos:
                doc.add_paragraph("Registro Fotográfico:")
                img_stream = io.BytesIO(st.session_state.fotos[foto_key].getvalue())
                doc.add_picture(img_stream, width=Inches(4))

        # Salva o arquivo em memória para download
        target = io.BytesIO()
        doc.save(target)
        
        st.download_button(
            label="💾 BAIXAR ARQUIVO WORD",
            data=target.getvalue(),
            file_name=f"Vistoria_{st.session_state.info_geral['end']}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
