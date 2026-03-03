import streamlit as st
from docx import Document
from docx.shared import Inches
import io

# Configuração da Página
st.set_page_config(page_title="Vistoria Pro", page_icon="📋", layout="centered")

# --- CSS PROFISSIONAL (BASE44 STYLE) ---
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
            if c2.button("🗑️ Deletar", key=f"del_{idx}"):
                st.session_state.historico.pop(idx); st.rerun()
            st.download_button("📥 Baixar Novamente", item['data_doc'], f"{item['nome']}.docx", key=f"dl_{idx}")

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
    
    ESTADOS = ["Em bom estado", "Novo", "Avarias leves", "Avarias graves"]
    CORES = ["Branca", "Gelo", "Cinza", "Bege", "Preta", "Madeira", "Off-white"]

    for i, nome_comodo in enumerate(st.session_state.comodos):
        with tabs[i]:
            kb = f"{nome_comodo}_{i}" # Chave única para salvar na memória
            
            # --- PISO E RODAPÉ ---
            with st.expander("🏗️ Piso e Rodapé", expanded=True):
                c1, c2 = st.columns(2)
                p_mat = c1.selectbox("Material Piso", ["Porcelanato", "Cerâmico", "Laminado", "Vinílico"], key=f"p_mat_{kb}")
                p_cor = c2.selectbox("Cor do Piso", CORES, key=f"p_cor_{kb}")
                p_est = st.selectbox("Estado do Piso", ESTADOS, key=f"p_est_{kb}")
                
                c3, c4 = st.columns(2)
                r_mat = c3.selectbox("Material Rodapé", ["Mesmo do piso", "Madeira/MDF", "PVC"], key=f"r_mat_{kb}")
                r_est = c4.selectbox("Estado Rodapé", ESTADOS, key=f"r_est_{kb}")
                
                f_piso = st.file_uploader("📷 Foto Piso/Rodapé", type=['jpg', 'png'], key=f"f_piso_{kb}")
                if f_piso: st.session_state.fotos_db[f"f_piso_{kb}"] = f_piso

            # --- PAREDES E TETO ---
            with st.expander("🎨 Paredes e Teto"):
                c1, c2 = st.columns(2)
                pa_cor = c1.selectbox("Cor Paredes", CORES, key=f"pa_cor_{kb}")
                pa_est = c2.selectbox("Estado Paredes", ESTADOS, key=f"pa_est_{kb}")
                
                t_est = st.selectbox("Estado Teto", ESTADOS, key=f"t_est_{kb}")
                gesso = st.checkbox("Possui moldura de gesso?", key=f"gesso_{kb}")
                
                f_parede = st.file_uploader("📷 Foto Paredes/Teto", type=['jpg', 'png'], key=f"f_parede_{kb}")
                if f_parede: st.session_state.fotos_db[f"f_parede_{kb}"] = f_parede

            # --- PORTA E JANELA ---
            with st.expander("🚪 Aberturas"):
                st.write("**Porta**")
                c1, c2, c3 = st.columns(3)
                po_est = c1.selectbox("Folha Porta", ESTADOS, key=f"po_est_{kb}")
                ba_est = c2.selectbox("Batente", ESTADOS, key=f"ba_est_{kb}")
                fe_est = c3.selectbox("Fechadura", ESTADOS, key=f"fe_est_{kb}")
                ch_qtd = st.number_input("Qtd Chaves", 0, 5, key=f"ch_qtd_{kb}")
                
                st.write("**Janela**")
                ja_est = st.selectbox("Estado Janela/Vidros", ESTADOS, key=f"ja_est_{kb}")
                
                f_aber = st.file_uploader("📷 Foto Aberturas", type=['jpg', 'png'], key=f"f_aber_{kb}")
                if f_aber: st.session_state.fotos_db[f"f_aber_{kb}"] = f_aber

            # --- ELÉTRICA E LUZ ---
            with st.expander("💡 Elétrica e Iluminação"):
                c1, c2 = st.columns(2)
                tom_qtd = c1.number_input("Qtd Tomadas", 0, 30, key=f"tom_qtd_{kb}")
                tom_est = c2.selectbox("Estado Espelhos", ESTADOS, key=f"tom_est_{kb}")
                
                l_tip = st.selectbox("Tipo Luminária", ["Plafon", "Spot", "Painel LED"], key=f"l_tip_{kb}")
                l_fun = st.radio("Status Luz", ["Funcionando", "Queimada", "Faltante"], key=f"l_fun_{kb}", horizontal=True)
                
                f_ele = st.file_uploader("📷 Foto Elétrica/Luz", type=['jpg', 'png'], key=f"f_ele_{kb}")
                if f_ele: st.session_state.fotos_db[f"f_ele_{kb}"] = f_ele

            st.text_area("Observações Adicionais", key=f"obs_{kb}")

    if st.button("🚀 FINALIZAR E GERAR RELATÓRIO"):
        doc = Document()
        doc.add_heading('RELATÓRIO DE VISTORIA', 0)
        doc.add_paragraph(f"IMÓVEL: {st.session_state.info_geral['end']}")
        doc.add_paragraph(f"DATA: {st.session_state.info_geral['data']} | TIPO: {st.session_state.info_geral['tipo']}")

        for i, nome in enumerate(st.session_state.comodos):
            kb = f"{nome}_{i}"
            doc.add_heading(nome.upper(), level=1)
            
            # --- CONSTRUÇÃO DO TEXTO DESCRITIVO ---
            p = doc.add_paragraph()
            p.add_run(f"Piso {st.session_state.get(f'p_mat_{kb}')} na cor {st.session_state.get(f'p_cor_{kb}')}, {st.session_state.get(f'p_est_{kb}')}. ").bold = False
            p.add_run(f"Rodapé em {st.session_state.get(f'r_mat_{kb}')}, {st.session_state.get(f'r_est_{kb}')}. ")
            p.add_run(f"Paredes na cor {st.session_state.get(f'pa_cor_{kb}')}, {st.session_state.get(f'pa_est_{kb}')}. ")
            p.add_run(f"Teto {st.session_state.get(f't_est_{kb}')}{' com moldura de gesso' if st.session_state.get(f'gesso_{kb}') else ''}. ")
            p.add_run(f"Porta {st.session_state.get(f'po_est_{kb}')}, batente {st.session_state.get(f'ba_est_{kb}')} e fechadura {st.session_state.get(f'fe_est_{kb}')}, com {st.session_state.get(f'ch_qtd_{kb}')} chave(s). ")
            p.add_run(f"Janela {st.session_state.get(f'ja_est_{kb}')}. ")
            p.add_run(f"Elétrica com {st.session_state.get(f'tom_qtd_{kb}')} tomadas {st.session_state.get(f'tom_est_{kb}')}. ")
            p.add_run(f"Iluminação tipo {st.session_state.get(f'l_tip_{kb}')} {st.session_state.get(f'l_fun_{kb}')}. ")
            
            obs = st.session_state.get(f"obs_{kb}")
            if obs: doc.add_paragraph(f"OBSERVAÇÕES: {obs}")

            # --- FOTOS LADO A LADO (2 POR LINHA) ---
            fotos_comodo = []
            for aux in ["f_piso", "f_parede", "f_aber", "f_ele"]:
                if f"{aux}_{kb}" in st.session_state.fotos_db:
                    fotos_comodo.append(st.session_state.fotos_db[f"{aux}_{kb}"])

            if fotos_comodo:
                doc.add_paragraph("\nREGISTROS FOTOGRÁFICOS:")
                for j in range(0, len(fotos_comodo), 2):
                    table = doc.add_table(rows=1, cols=2)
                    for idx, photo in enumerate(fotos_comodo[j:j+2]):
                        img_stream = io.BytesIO(photo.getvalue())
                        cell = table.rows[0].cells[idx]
                        run = cell.paragraphs[0].add_run()
                        run.add_picture(img_stream, width=Inches(3.0))

        target = io.BytesIO()
        doc.save(target)
        doc_bytes = target.getvalue()

        # Histórico
        st.session_state.historico.insert(0, {"nome": st.session_state.info_geral['end'][:20], "data": st.session_state.info_geral['data'], "data_doc": doc_bytes})
        if len(st.session_state.historico) > 2: st.session_state.historico.pop()
        
        st.success("Relatório Gerado!")
        st.download_button("💾 Baixar Word", doc_bytes, "vistoria_completa.docx")
