import streamlit as st
from docx import Document
from docx.shared import Inches
import io

# Configuração da Página
st.set_page_config(page_title="Vistoria Pro", page_icon="📋", layout="centered")

# --- CSS ESTILO PROFISSIONAL ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    header {visibility: hidden;}
    .main-header {
        background-color: #1a202c; padding: 15px; color: white;
        text-align: center; font-size: 1.5rem; font-weight: bold;
        border-radius: 0 0 10px 10px; margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] { background-color: #f1f5f9; border-radius: 8px; font-weight: 600; }
    .stTabs [aria-selected="true"] { background-color: #2563eb !important; color: white !important; }
    </style>
    <div class="main-header">📋 Vistoria Pro</div>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE MEMÓRIA ---
if 'etapa' not in st.session_state: st.session_state.etapa = 1
if 'historico' not in st.session_state: st.session_state.historico = []
if 'fotos_db' not in st.session_state: st.session_state.fotos_db = {}

def resetar_vistoria():
    for key in list(st.session_state.keys()):
        if key not in ['historico']: del st.session_state[key]
    st.session_state.etapa = 1
    st.rerun()

# --- NAVEGAÇÃO E HISTÓRICO ---
col_ini, col_hist = st.columns([1, 1])
if col_ini.button("🏠 Novo / Início"): resetar_vistoria()

with st.expander("🕒 Vistorias Recentes (Máx. 2)"):
    if not st.session_state.historico: st.write("Nenhuma vistoria no histórico.")
    else:
        for idx, item in enumerate(st.session_state.historico):
            c1, c2 = st.columns([3, 1])
            c1.write(f"**{item['nome']}** ({item['data']})")
            if c2.button("🗑️", key=f"del_{idx}"):
                st.session_state.historico.pop(idx)
                st.rerun()
            st.download_button("📥 Baixar Documento", item['data_doc'], f"{item['nome']}.docx", key=f"dl_{idx}")

# --- ETAPA 1: IDENTIFICAÇÃO ---
if st.session_state.etapa == 1:
    st.subheader("📄 Identificação")
    with st.expander("📍 Dados do Imóvel", expanded=True):
        end = st.text_input("Endereço Completo", key="main_end")
        c1, c2 = st.columns(2)
        data_v = c1.date_input("Data")
        tipo_v = c2.selectbox("Tipo", ["Entrada", "Saída"])
        if st.button("Continuar"):
            if end:
                st.session_state.info_geral = {"end": end, "data": str(data_v), "tipo": tipo_v}
                st.session_state.etapa = 2
                st.rerun()

# --- ETAPA 2: CÔMODOS ---
elif st.session_state.etapa == 2:
    st.subheader("🏠 Seleção de Cômodos")
    opcoes = ["Sala", "Cozinha", "Banheiro Social", "Área de Serviço", "Corredor", "Garagem", "Sacada"]
    selecionados = [item for item in opcoes if st.checkbox(item, key=f"sel_{item}")]
    
    c1, c2 = st.columns(2)
    q = c1.number_input("Quartos", 0, 10, 1)
    s = c2.number_input("Suítes", 0, 10, 0)
    
    if st.button("Iniciar Preenchimento"):
        lista = selecionados + [f"Quarto {i+1}" for i in range(q)]
        for i in range(s):
            lista.append(f"Suíte {i+1}"); lista.append(f"Banheiro Suíte {i+1}")
        st.session_state.comodos = lista
        st.session_state.etapa = 3
        st.rerun()

# --- ETAPA 3: VISTORIA DETALHADA ---
elif st.session_state.etapa == 3:
    st.info(f"📍 {st.session_state.info_geral['end']}")
    tabs = st.tabs(st.session_state.comodos)
    
    ESTADOS = ["Bom estado", "Novo", "Avarias", "Faltante"]

    for i, nome_comodo in enumerate(st.session_state.comodos):
        with tabs[i]:
            kb = f"{nome_comodo}_{i}"
            
            def campo_com_foto(label_item, key_suffix):
                with st.expander(label_item):
                    c1, c2 = st.columns(2)
                    res = c1.selectbox(f"Estado {label_item}", ESTADOS, key=f"est_{key_suffix}_{kb}")
                    foto = c2.file_uploader("📷 Foto", type=['jpg', 'png'], key=f"f_{key_suffix}_{kb}")
                    if foto: st.session_state.fotos_db[f"f_{key_suffix}_{kb}"] = foto
                    return res

            # Itens Detalhados
            res_piso = campo_com_foto("🏗️ Piso", "piso")
            res_roda = campo_com_foto("📐 Rodapé", "roda")
            res_pare = campo_com_foto("🎨 Paredes", "pare")
            res_teto = campo_com_foto("🔝 Teto", "teto")
            res_port = campo_com_foto("🚪 Porta", "port")
            res_jane = campo_com_foto("🪟 Janela", "jane")
            res_ilum = campo_com_foto("💡 Iluminação", "ilum")
            res_elet = campo_com_foto("⚡ Elétrica", "elet")

            st.text_area("Notas Adicionais", key=f"obs_{kb}")

    if st.button("🚀 FINALIZAR E GERAR RELATÓRIO"):
        doc = Document()
        doc.add_heading('RELATÓRIO DE VISTORIA', 0)
        doc.add_paragraph(f"IMÓVEL: {st.session_state.info_geral['end']}")

        for i, nome in enumerate(st.session_state.comodos):
            kb = f"{nome}_{i}"
            doc.add_heading(nome.upper(), level=1)
            
            # Lista para organizar as fotos lado a lado
            fotos_comodo = []
            itens = ["piso", "roda", "pare", "teto", "port", "jane", "ilum", "elet"]
            
            for it in itens:
                estado = st.session_state.get(f"est_{it}_{kb}")
                doc.add_paragraph(f"• {it.capitalize()}: {estado}")
                if f"f_{it}_{kb}" in st.session_state.fotos_db:
                    fotos_comodo.append(st.session_state.fotos_db[f"f_{it}_{kb}"])

            # Inserção de fotos lado a lado (2 por linha)
            if fotos_comodo:
                doc.add_paragraph("\nREGISTROS FOTOGRÁFICOS:")
                for j in range(0, len(fotos_comodo), 2):
                    table = doc.add_table(rows=1, cols=2)
                    for idx, photo in enumerate(fotos_comodo[j:j+2]):
                        img_stream = io.BytesIO(photo.getvalue())
                        cell = table.rows[0].cells[idx]
                        paragraph = cell.paragraphs[0]
                        run = paragraph.add_run()
                        run.add_picture(img_stream, width=Inches(3.0)) # Redimensionamento automático

        target = io.BytesIO()
        doc.save(target)
        doc_bytes = target.getvalue()

        # Salva no histórico (últimas 2)
        st.session_state.historico.insert(0, {"nome": st.session_state.info_geral['end'][:20], "data": st.session_state.info_geral['data'], "data_doc": doc_bytes})
        if len(st.session_state.historico) > 2: st.session_state.historico.pop()
        
        st.success("Relatório Pronto!")
        st.download_button("💾 Baixar Word", doc_bytes, "vistoria_pro.docx")
