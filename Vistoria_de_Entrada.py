import streamlit as st
from docx import Document
from docx.shared import Inches
import io

# Configuração da Página
st.set_page_config(page_title="Vistoria Pro", page_icon="📋", layout="centered")

# --- CSS ESTILO BASE44 ---
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
    .historico-card { 
        background-color: white; padding: 10px; border-radius: 10px; 
        border: 1px solid #e2e8f0; margin-bottom: 10px;
    }
    </style>
    <div class="main-header">📋 Vistoria Pro</div>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE MEMÓRIA ---
if 'etapa' not in st.session_state: st.session_state.etapa = 1
if 'historico' not in st.session_state: st.session_state.historico = []
if 'fotos' not in st.session_state: st.session_state.fotos = {}

def resetar_vistoria():
    for key in list(st.session_state.keys()):
        if key not in ['historico', 'etapa_historico']: # Mantém o histórico
            del st.session_state[key]
    st.session_state.etapa = 1
    st.rerun()

# --- BARRA SUPERIOR DE AÇÕES ---
col_ini, col_hist = st.columns([1, 1])
if col_ini.button("🏠 Voltar ao Início"):
    resetar_vistoria()

# --- SEÇÃO DE HISTÓRICO (2 ÚLTIMAS) ---
with st.expander("🕒 Histórico de Vistorias (Recentes)"):
    if not st.session_state.historico:
        st.write("Nenhuma vistoria gerada nesta sessão.")
    else:
        for idx, item in enumerate(st.session_state.historico):
            with st.container():
                st.markdown(f"**{item['nome']}** - {item['data']}")
                c1, c2 = st.columns(2)
                c1.download_button("📥 Baixar", item['data_doc'], f"{item['nome']}.docx", key=f"dl_{idx}")
                if c2.button("🗑️ Deletar", key=f"del_{idx}"):
                    st.session_state.historico.pop(idx)
                    st.rerun()
                st.markdown("---")

# --- ETAPA 1: INFORMAÇÕES BÁSICAS ---
if st.session_state.etapa == 1:
    st.subheader("📄 Nova Vistoria")
    with st.expander("📍 Identificação do Imóvel", expanded=True):
        end = st.text_input("Endereço Completo", placeholder="Rua, Número, Apto...", key="main_end")
        c1, c2 = st.columns(2)
        data_v = c1.date_input("Data da Vistoria")
        tipo_v = c2.selectbox("Tipo de Vistoria", ["Entrada", "Saída", "Conferência"])
        
        if st.button("Continuar"):
            if end:
                st.session_state.info_geral = {"end": end, "data": str(data_v), "tipo": tipo_v}
                st.session_state.etapa = 2
                st.rerun()
            else:
                st.error("Preencha o endereço para continuar.")

# --- ETAPA 2: CONFIGURAÇÃO DE CÔMODOS ---
elif st.session_state.etapa == 2:
    st.subheader("🏠 Quais cômodos vamos vistoriar?")
    opcoes = ["Sala", "Cozinha", "Banheiro Social", "Área de Serviço", "Corredor", "Garagem", "Sacada / Varanda"]
    selecionados = []
    
    col_a, col_b = st.columns(2)
    for i, item in enumerate(opcoes):
        col = col_a if i % 2 == 0 else col_b
        if col.checkbox(item, key=f"sel_{item}"): selecionados.append(item)
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    q = c1.number_input("Quantidade de Quartos", 0, 10, 1)
    s = c2.number_input("Quantidade de Suítes", 0, 10, 0)
    
    if st.button(f"Iniciar Preenchimento"):
        lista = selecionados + [f"Quarto {i+1}" for i in range(q)]
        for i in range(s):
            lista.append(f"Suíte {i+1}")
            lista.append(f"Banheiro Suíte {i+1}")
        st.session_state.comodos = lista
        st.session_state.etapa = 3
        st.rerun()

# --- ETAPA 3: PREENCHIMENTO DETALHADO ---
elif st.session_state.etapa == 3:
    st.info(f"📍 {st.session_state.info_geral['end']}")
    tabs = st.tabs(st.session_state.comodos)
    
    ESTADOS = ["Em bom estado", "Novo", "Avarias leves", "Avarias graves", "Faltante"]
    CORES = ["Branca", "Gelo", "Cinza", "Bege", "Preta", "Madeira", "Off-white"]

    for i, nome_comodo in enumerate(st.session_state.comodos):
        with tabs[i]:
            kb = f"{nome_comodo}_{i}" # Chave base para salvamento automático
            
            # 🏗️ PISO E RODAPÉ
            with st.expander("🏗️ Piso e Rodapé", expanded=True):
                c1, c2 = st.columns(2)
                c1.selectbox("Material Piso", ["Porcelanato", "Cerâmico", "Laminado", "Vinílico"], key=f"p_mat_{kb}")
                c2.selectbox("Estado Piso", ESTADOS, key=f"p_est_{kb}")
                
                c3, c4 = st.columns(2)
                c3.selectbox("Rodapé Estado", ESTADOS, key=f"r_est_{kb}")
                c4.selectbox("Cor Geral", CORES, key=f"cor_{kb}")

            # 🎨 PAREDES E TETO
            with st.expander("🎨 Paredes e Teto"):
                c1, c2 = st.columns(2)
                c1.selectbox("Pintura Parede", ESTADOS, key=f"par_est_{kb}")
                c2.selectbox("Estado Teto", ESTADOS, key=f"te_est_{kb}")
                st.checkbox("Possui moldura de gesso?", key=f"gesso_{kb}")

            # 🚪 PORTA E JANELA
            with st.expander("🚪 Aberturas (Porta/Janela)"):
                st.write("**Porta**")
                c1, c2, c3 = st.columns(3)
                c1.selectbox("Folha", ESTADOS, key=f"po_est_{kb}")
                c2.selectbox("Batente", ESTADOS, key=f"bat_est_{kb}")
                c3.selectbox("Fechadura", ESTADOS, key=f"fec_est_{kb}")
                
                st.write("**Janela**")
                c4, c5 = st.columns(2)
                c4.selectbox("Vidros/Trincos", ESTADOS, key=f"ja_est_{kb}")
                c5.number_input("Qtd Chaves", 0, 5, key=f"ch_qtd_{kb}")

            # 💡 ELÉTRICA E LUZ
            with st.expander("💡 Elétrica e Iluminação"):
                c1, c2 = st.columns(2)
                c1.number_input("Qtd Tomadas", 0, 20, key=f"tom_qtd_{kb}")
                c2.selectbox("Estado Espelhos", ESTADOS, key=f"tom_est_{kb}")
                
                st.selectbox("Tipo de Lâmpada/Luminária", ["Plafon", "Spot LED", "Painel"], key=f"lum_tip_{kb}")
                st.radio("Status Luz", ["Funcionando", "Queimada", "Faltante"], key=f"lum_stat_{kb}", horizontal=True)

            # 📷 FOTOS E OBS
            st.write("📷 **Registros do Cômodo**")
            f_u = st.file_uploader("Anexar foto principal", type=['jpg', 'png'], key=f"f_u_{kb}")
            if f_u: st.session_state.fotos[f"f_u_{kb}"] = f_u
            
            st.text_area("Observações Adicionais", key=f"obs_{kb}", placeholder="Descreva riscos, manchas ou detalhes...")

    st.markdown("---")
    if st.button("🚀 FINALIZAR E GERAR WORD"):
        doc = Document()
        doc.add_heading('RELATÓRIO DE VISTORIA', 0)
        doc.add_paragraph(f"IMÓVEL: {st.session_state.info_geral['end']}")
        doc.add_paragraph(f"DATA: {st.session_state.info_geral['data']} | TIPO: {st.session_state.info_geral['tipo']}")

        for i, nome in enumerate(st.session_state.comodos):
            kb = f"{nome}_{i}"
            doc.add_heading(nome.upper(), level=1)
            
            # Coleta de dados da memória
            p_m = st.session_state.get(f"p_mat_{kb}")
            p_e = st.session_state.get(f"p_est_{kb}")
            doc.add_paragraph(f"PISO: {p_m} em estado {p_e}.")
            
            # Adiciona foto se houver
            if f"f_u_{kb}" in st.session_state.fotos:
                img_data = io.BytesIO(st.session_state.fotos[f"f_u_{kb}"].getvalue())
                doc.add_picture(img_data, width=Inches(3.5))
            
            doc.add_paragraph(f"OBSERVAÇÕES: {st.session_state.get(f'obs_{kb}', 'Nada a declarar.')}")

        target = io.BytesIO()
        doc.save(target)
        doc_bytes = target.getvalue()

        # Salva no Histórico (Mantém apenas as 2 últimas)
        nova_vistoria = {
            "nome": st.session_state.info_geral['end'][:30], 
            "data": st.session_state.info_geral['data'],
            "data_doc": doc_bytes
        }
        st.session_state.historico.insert(0, nova_vistoria)
        if len(st.session_state.historico) > 2:
            st.session_state.historico.pop()
        
        st.success("Relatório gerado! Use o botão abaixo ou veja no Histórico acima.")
        st.download_button("💾 BAIXAR AGORA", doc_bytes, "vistoria_final.docx")
