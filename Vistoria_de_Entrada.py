import streamlit as st
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# Configuração da Página
st.set_page_config(page_title="Vistoria Técnica Pro", page_icon="🏢", layout="wide")

# --- ESTILO CSS CUSTOMIZADO ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    .main-header {
        background-color: #0f172a; padding: 20px; color: white;
        text-align: center; font-size: 1.8rem; font-weight: bold;
        border-radius: 0 0 15px 15px; margin-bottom: 30px;
    }
    .section-card {
        background-color: white; padding: 20px; border-radius: 12px;
        border-left: 5px solid #2563eb; margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab"] { font-size: 1.1rem; font-weight: 700; }
    </style>
    <div class="main-header">🏢 Sistema de Vistoria Técnica Imobiliária</div>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADOS ---
if 'etapa' not in st.session_state: st.session_state.etapa = 1
if 'historico' not in st.session_state: st.session_state.historico = []
if 'fotos_db' not in st.session_state: st.session_state.fotos_db = {}

# --- NAVEGAÇÃO SUPERIOR ---
if st.session_state.etapa > 1:
    if st.sidebar.button("🏠 Reiniciar Vistoria"):
        for key in list(st.session_state.keys()):
            if key != 'historico': del st.session_state[key]
        st.session_state.etapa = 1
        st.rerun()

# --- ETAPA 1: CABEÇALHO ---
if st.session_state.etapa == 1:
    st.subheader("📋 Dados da Vistoria")
    with st.form("identificacao"):
        end = st.text_input("Endereço Completo do Imóvel", placeholder="Ex: Av. Paulista, 1000 - Apto 51")
        c1, c2, c3 = st.columns(3)
        data_v = c1.date_input("Data da Inspeção")
        tipo_v = c2.selectbox("Finalidade", ["Entrada", "Saída", "Venda", "Renovação"])
        vistoriador = c3.text_input("Nome do Vistoriador")
        if st.form_submit_button("Configurar Cômodos ➡️"):
            if end and vistoriador:
                st.session_state.info_geral = {"end": end, "data": str(data_v), "tipo": tipo_v, "nome": vistoriador}
                st.session_state.etapa = 2
                st.rerun()
            else: st.error("Por favor, preencha o endereço e o nome do vistoriador.")

# --- ETAPA 2: CONFIGURAÇÃO DO IMÓVEL ---
elif st.session_state.etapa == 2:
    st.subheader("🏠 Composição do Imóvel")
    st.info("Selecione os ambientes que compõem este imóvel:")
    
    opcoes_base = ["Sala de Estar", "Sala de Jantar", "Cozinha", "Área de Serviço", "Banheiro Social", "Lavabo", "Corredor", "Sacada/Varanda", "Garagem", "Depósito"]
    selecionados = []
    
    cols = st.columns(3)
    for i, item in enumerate(opcoes_base):
        if cols[i % 3].checkbox(item, key=f"sel_{item}"): selecionados.append(item)
    
    c1, c2 = st.columns(2)
    q_quartos = c1.number_input("Dormitórios (Simples)", 0, 10, 1)
    q_suites = c2.number_input("Suítes", 0, 10, 0)
    
    if st.button("Ir para Inspeção Detalhada 📝"):
        ambientes = selecionados + [f"Dormitório {i+1}" for i in range(q_quartos)]
        for i in range(q_suites):
            ambientes.append(f"Suíte {i+1}")
            ambientes.append(f"Banheiro Suíte {i+1}")
        st.session_state.comodos = ambientes
        st.session_state.etapa = 3
        st.rerun()

# --- ETAPA 3: INSPEÇÃO TÉCNICA (O CORAÇÃO DO APP) ---
elif st.session_state.etapa == 3:
    st.caption(f"Imóvel: {st.session_state.info_geral['end']}")
    tabs = st.tabs(st.session_state.comodos)
    
    # OPÇÕES TÉCNICAS EXPANDIDAS
    ESTADOS = ["Novo (Sem uso)", "Excelente", "Bom (Marcas leves)", "Regular (Desgastado)", "Avariado (Precisa reparo)", "Crítico (Substituir)"]
    MAT_PISO = ["Porcelanato Polido", "Porcelanato Acetinado", "Cerâmica", "Laminado", "Vinílico", "Madeira Maciça", "Taco", "Ardósia", "Mármore", "Granito", "Cimento Queimado", "Carpete"]
    MAT_BANCADA = ["Granito", "Mármore", "Inox", "Silestone/Quartzo", "Madeira Tratada", "Concreto", "MDF Revestido"]

    for i, nome in enumerate(st.session_state.comodos):
        with tabs[i]:
            kb = f"{nome}_{i}"
            
            # --- FUNÇÃO INTERNA PARA GERAR CAMPOS COM FOTOS ---
            def criar_item_vistoria(titulo, prefixo, options_mat=None):
                with st.expander(f"🔍 {titulo}", expanded=False):
                    presente = st.checkbox("Presente / Aplicável", value=True, key=f"pres_{prefixo}_{kb}")
                    if presente:
                        c1, c2, c3 = st.columns([1, 1, 2])
                        if options_mat:
                            mat = c1.selectbox("Material", options_mat, key=f"mat_{prefixo}_{kb}")
                        else: mat = None
                        
                        est = c2.selectbox("Estado", ESTADOS, key=f"est_{prefixo}_{kb}")
                        detalhe = c3.text_input("Detalhes (Ricos, manchas, marcas)", key=f"det_{prefixo}_{kb}")
                        
                        foto = st.file_uploader(f"Anexar Foto - {titulo}", type=['jpg', 'png'], key=f"f_up_{prefixo}_{kb}")
                        if foto: st.session_state.fotos_db[f"f_{prefixo}_{kb}"] = foto
                        return {"presente": True, "mat": mat, "est": est, "det": detalhe}
                    return {"presente": False}

            # INVENTÁRIO DO CÔMODO
            st.markdown("### Estrutura")
            res_piso = criar_item_vistoria("Piso", "piso", MAT_PISO)
            res_roda = criar_item_vistoria("Rodapé", "roda", ["MDF", "PVC", "Mesmo do Piso", "Madeira"])
            res_pare = criar_item_vistoria("Paredes (Pintura/Revestimento)", "pare", ["Tinta Látex", "Tinta Acrílica", "Papel de Parede", "Azulejo"])
            res_teto = criar_item_vistoria("Teto e Gesso", "teto", ["Gesso Liso", "Forro PVC", "Moldura Gesso", "Sanca Aberta"])
            
            st.markdown("### Aberturas")
            res_port = criar_item_vistoria("Porta e Guarnições", "port", ["Madeira Puxador", "Madeira Simples", "Vidro/Blindex", "Alumínio"])
            res_jane = criar_item_vistoria("Janela e Persianas", "jane", ["Alumínio", "Madeira", "PVC c/ Persiana", "Ferro"])
            
            st.markdown("### Instalações")
            res_elet = criar_item_vistoria("Elétrica (Tomadas/Espelhos)", "elet")
            res_ilum = criar_item_vistoria("Iluminação", "ilum", ["Plafon LED", "Spot", "Lustre", "Painel Embutir"])
            
            # Condicional para Áreas Molhadas
            if any(x in nome for x in ["Cozinha", "Banheiro", "Serviço", "Lavabo"]):
                st.markdown("### Áreas Molhadas / Metais")
                res_banc = criar_item_vistoria("Bancada e Pia", "banc", MAT_BANCADA)
                res_meta = criar_item_vistoria("Metais (Torneiras/Registros)", "meta")
                res_louc = criar_item_vistoria("Louças (Vaso/Cuba)", "louc")
                res_arma = criar_item_vistoria("Armários Planejados", "arma")

            # --- GERAÇÃO DO WORD ---
            st.divider()
            if st.button("📊 FINALIZAR VISTORIA E GERAR LAUDO", type="primary"):
                doc = Document()
                
                # Cabeçalho do Documento
                section = doc.sections[0]
                header = section.header
                header.paragraphs[0].text = f"Laudo de Vistoria - {st.session_state.info_geral['tipo']}"
                
                doc.add_heading('RELATÓRIO TÉCNICO DE VISTORIA IMOBILIÁRIA', 0)
                
                # Dados Gerais
                table_info = doc.add_table(rows=2, cols=2)
                table_info.style = 'Table Grid'
                table_info.cell(0,0).text = f"Imóvel: {st.session_state.info_geral['end']}"
                table_info.cell(0,1).text = f"Data: {st.session_state.info_geral['data']}"
                table_info.cell(1,0).text = f"Vistoriador: {st.session_state.info_geral['nome']}"
                table_info.cell(1,1).text = f"Tipo: {st.session_state.info_geral['tipo']}"

                for i_amb, nome_amb in enumerate(st.session_state.comodos):
                    kb_amb = f"{nome_amb}_{i_amb}"
                    doc.add_heading(nome_amb.upper(), level=1)
                    
                    # Coleta de dados e montagem de texto descritivo
                    texto_completo = []
                    fotos_amb = []
                    
                    itens_verificar = [
                        ("piso", "Piso"), ("roda", "Rodapé"), ("pare", "Paredes"), ("teto", "Teto"), 
                        ("port", "Porta"), ("jane", "Janela"), ("elet", "Elétrica"), ("ilum", "Iluminação"),
                        ("banc", "Bancada"), ("meta", "Metais"), ("louc", "Louças"), ("arma", "Armários")
                    ]
                    
                    for pref, label in itens_verificar:
                        if st.session_state.get(f"pres_{pref}_{kb_amb}"):
                            m = st.session_state.get(f"mat_{pref}_{kb_amb}", "")
                            e = st.session_state.get(f"est_{pref}_{kb_amb}", "")
                            d = st.session_state.get(f"det_{pref}_{kb_amb}", "")
                            
                            desc = f"{label}: {m} em estado {e}. "
                            if d: desc += f"Observação: {d}. "
                            texto_completo.append(desc)
                            
                            # Foto
                            if f"f_{pref}_{kb_amb}" in st.session_state.fotos_db:
                                fotos_amb.append(st.session_state.fotos_db[f"f_{pref}_{kb_amb}"])
                    
                    doc.add_paragraph("".join(texto_completo))
                    
                    # Inserção de Fotos em Grade 2x2
                    if fotos_amb:
                        doc.add_paragraph("REGISTRO FOTOGRÁFICO:")
                        table_fotos = doc.add_table(rows=(len(fotos_amb)+1)//2, cols=2)
                        for idx_f, f_data in enumerate(fotos_amb):
                            row = idx_f // 2
                            col = idx_f % 2
                            paragraph = table_fotos.rows[row].cells[col].paragraphs[0]
                            run = paragraph.add_run()
                            img_stream = io.BytesIO(f_data.getvalue())
                            run.add_picture(img_stream, width=Inches(3.0))

                # Footer / Assinaturas
                doc.add_page_break()
                doc.add_heading("Assinaturas", level=1)
                doc.add_paragraph("\n\n__________________________________________\nVistoriador Responsável")
                doc.add_paragraph("\n\n__________________________________________\nLocatário / Proprietário")

                target = io.BytesIO()
                doc.save(target)
                
                st.success("✅ Relatório gerado com sucesso!")
                st.download_button("📥 BAIXAR RELATÓRIO WORD (.DOCX)", target.getvalue(), f"Vistoria_{nome_amb}.docx")
