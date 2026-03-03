import streamlit as st
from docx import Document
from docx.shared import Inches
import io

# Configuração da Página
st.set_page_config(page_title="Vistoria Pro v16", page_icon="🏠", layout="centered")

# --- CSS AVANÇADO (ESTILO DASHBOARD) ---
st.markdown("""
    <style>
    .stApp { background-color: #f1f5f9; }
    header {visibility: hidden;}
    .main-header {
        background-color: #1e293b; padding: 20px; color: white;
        text-align: center; font-size: 1.6rem; font-weight: bold;
        border-radius: 0 0 15px 15px; margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background: transparent; }
    .stTabs [data-baseweb="tab"] { 
        background-color: white; border-radius: 10px; padding: 10px 20px;
        border: 1px solid #e2e8f0; font-weight: 600;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #2563eb !important; color: white !important; border: none;
    }
    div[data-testid="stExpander"] {
        background-color: white !important; border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important; margin-bottom: 10px !important;
    }
    </style>
    <div class="main-header">🏠 Vistoria Profissional</div>
    """, unsafe_allow_html=True)

# --- MEMÓRIA E ESTADOS ---
if 'etapa' not in st.session_state: st.session_state.etapa = 1
if 'historico' not in st.session_state: st.session_state.historico = []
if 'fotos_db' not in st.session_state: st.session_state.fotos_db = {}

def resetar():
    for key in list(st.session_state.keys()):
        if key not in ['historico']: del st.session_state[key]
    st.session_state.etapa = 1
    st.rerun()

# --- BARRA DE HISTÓRICO ---
with st.expander("🕒 Minhas Vistorias Recentes"):
    if not st.session_state.historico: st.info("Nenhuma vistoria salva.")
    else:
        for idx, item in enumerate(st.session_state.historico):
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(f"📍 {item['nome']}")
            c2.download_button("📥 Baixar", item['data_doc'], f"vistoria_{idx}.docx", key=f"dl_{idx}")
            if c3.button("🗑️", key=f"del_{idx}"):
                st.session_state.historico.pop(idx); st.rerun()

if st.session_state.etapa > 1:
    if st.button("⬅️ Voltar ao Início / Limpar"): resetar()

# --- ETAPA 1: IDENTIFICAÇÃO ---
if st.session_state.etapa == 1:
    st.subheader("1. Identificação")
    with st.container():
        end = st.text_input("Endereço do Imóvel", placeholder="Rua, Número, Bairro...", key="main_end")
        c1, c2 = st.columns(2)
        data_v = c1.date_input("Data da Vistoria")
        tipo_v = c2.selectbox("Tipo", ["Entrada", "Saída", "Conferência"])
        if st.button("Próximo Passo ➡️"):
            if end:
                st.session_state.info_geral = {"end": end, "data": str(data_v), "tipo": tipo_v}
                st.session_state.etapa = 2
                st.rerun()

# --- ETAPA 2: CÔMODOS ---
elif st.session_state.etapa == 2:
    st.subheader("2. Composição do Imóvel")
    opcoes = ["Sala", "Cozinha", "Banheiro Social", "Área de Serviço", "Corredor", "Varanda/Sacada", "Garagem"]
    selecionados = [item for item in opcoes if st.checkbox(item, key=f"sel_{item}")]
    
    c1, c2 = st.columns(2)
    q = c1.number_input("Quartos (Simples)", 0, 10, 1)
    s = c2.number_input("Suítes (Com Banheiro)", 0, 10, 0)
    
    if st.button("Iniciar Vistoria Detalhada 📝"):
        lista = selecionados + [f"Quarto {i+1}" for i in range(q)]
        for i in range(s):
            lista.append(f"Suíte {i+1}"); lista.append(f"Banheiro Suíte {i+1}")
        st.session_state.comodos = lista
        st.session_state.etapa = 3
        st.rerun()

# --- ETAPA 3: PREENCHIMENTO COMPLETO ---
elif st.session_state.etapa == 3:
    st.caption(f"📍 {st.session_state.info_geral['end']}")
    tabs = st.tabs(st.session_state.comodos)
    
    ESTADOS = ["Em bom estado", "Novo", "Usado (Marcas de uso)", "Com avarias", "Faltante"]
    CORES = ["Branca", "Gelo", "Bege", "Cinza", "Off-white", "Preta", "Madeira", "Natural"]

    for i, nome_comodo in enumerate(st.session_state.comodos):
        with tabs[i]:
            kb = f"{nome_comodo}_{i}" # Chave Única

            # 🏗️ PISO E RODAPÉ
            with st.expander("🏗️ Piso e Rodapé", expanded=True):
                c1, c2 = st.columns(2)
                p_mat = c1.selectbox("Material Piso", ["Porcelanato", "Cerâmico", "Laminado", "Vinílico", "Ardósia"], key=f"pm_{kb}")
                p_cor = c2.selectbox("Cor do Piso", CORES, key=f"pc_{kb}")
                p_est = st.selectbox("Estado do Piso", ESTADOS, key=f"pe_{kb}")
                
                c3, c4 = st.columns(2)
                r_inc = c3.checkbox("Possui Rodapé?", value=True, key=f"ri_{kb}")
                r_est = c4.selectbox("Estado Rodapé", ESTADOS, key=f"re_{kb}") if r_inc else "N/A"
                
                f_piso = st.file_uploader("📷 Foto Piso/Rodapé", type=['jpg', 'png'], key=f"fp_{kb}")
                if f_piso: st.session_state.fotos_db[f"fp_{kb}"] = f_piso

            # 🎨 PAREDES E TETO
            with st.expander("🎨 Paredes e Teto"):
                c1, c2 = st.columns(2)
                pa_cor = c1.selectbox("Cor Paredes", CORES, key=f"pac_{kb}")
                pa_est = c2.selectbox("Estado Paredes", ESTADOS, key=f"pae_{kb}")
                t_est = st.selectbox("Estado Teto", ESTADOS, key=f"te_{kb}")
                gesso = st.checkbox("Possui moldura de gesso?", key=f"gs_{kb}")
                
                f_par = st.file_uploader("📷 Foto Paredes/Teto", type=['jpg', 'png'], key=f"fpa_{kb}")
                if f_par: st.session_state.fotos_db[f"fpa_{kb}"] = f_par

            # 🚪 PORTA E JANELA
            with st.expander("🚪 Portas e Janelas"):
                st.write("**Detalhes da Porta**")
                c1, c2, c3 = st.columns(3)
                po_est = c1.selectbox("Folha", ESTADOS, key=f"poe_{kb}")
                ba_est = c2.selectbox("Batente", ESTADOS, key=f"bae_{kb}")
                fe_est = c3.selectbox("Maçaneta", ESTADOS, key=f"fee_{kb}")
                ch_qtd = st.number_input("Qtd Chaves", 0, 5, key=f"chq_{kb}")
                
                st.write("**Detalhes da Janela**")
                ja_est = st.selectbox("Estado Janela (Vidros/Trincos)", ESTADOS, key=f"jae_{kb}")
                
                f_ab = st.file_uploader("📷 Foto Aberturas", type=['jpg', 'png'], key=f"fab_{kb}")
                if f_ab: st.session_state.fotos_db[f"fab_{kb}"] = f_ab

            # 💡 ELÉTRICA E ILUMINAÇÃO
            with st.expander("💡 Elétrica e Iluminação"):
                c1, c2, c3 = st.columns(3)
                tom_q = c1.number_input("Qtd Tomadas", 0, 30, key=f"tq_{kb}")
                tom_e = c2.selectbox("Espelhos", ESTADOS, key=f"tep_{kb}")
                int_q = c3.number_input("Interruptores", 0, 20, key=f"iq_{kb}")
                
                st.write("**Luminária**")
                c4, c5 = st.columns(2)
                l_tip = c4.selectbox("Tipo", ["Plafon", "Spot LED", "Painel", "Lâmpada Simples"], key=f"lti_{kb}")
                l_est = c5.radio("Status", ["Funcionando", "Queimada", "Faltante"], key=f"lst_{kb}", horizontal=True)
                
                f_el = st.file_uploader("📷 Foto Elétrica", type=['jpg', 'png'], key=f"fel_{kb}")
                if f_el: st.session_state.fotos_db[f"fel_{kb}"] = f_el

            # ⚡ OUTROS (RALO E OBS)
            with st.expander("➕ Outros"):
                ralo = st.checkbox("Incluir Ralo?", key=f"ra_{kb}")
                obs = st.text_area("Observações Adicionais", key=f"ob_{kb}", placeholder="Riscados, manchas, etc...")

    # --- GERAÇÃO DO WORD ---
    if st.button("🚀 GERAR RELATÓRIO FINAL"):
        doc = Document()
        doc.add_heading('LAUDO DE VISTORIA IMOBILIÁRIA', 0)
        doc.add_paragraph(f"IMÓVEL: {st.session_state.info_geral['end']}")
        doc.add_paragraph(f"DATA: {st.session_state.info_geral['data']} | TIPO: {st.session_state.info_geral['tipo']}")

        for i, nome in enumerate(st.session_state.comodos):
            kb = f"{nome}_{i}"
            doc.add_heading(nome.upper(), level=1)
            
            # Montagem do Texto Descritivo
            txt = f"Piso {st.session_state.get(f'pm_{kb}')} cor {st.session_state.get(f'pc_{kb}')}, {st.session_state.get(f'pe_{kb}')}. "
            if st.session_state.get(f'ri_{kb}'):
                txt += f"Rodapé {st.session_state.get(f're_{kb}')}. "
            txt += f"Paredes cor {st.session_state.get(f'pac_{kb}')}, {st.session_state.get(f'pae_{kb}')}. "
            txt += f"Teto {st.session_state.get(f'te_{kb}')}{' com moldura de gesso' if st.session_state.get(f'gs_{kb}') else ''}. "
            txt += f"Porta {st.session_state.get(f'poe_{kb}')}, batente {st.session_state.get(f'bae_{kb}')}, fechadura {st.session_state.get(f'fee_{kb}')} com {st.session_state.get(f'chq_{kb}')} chave(s). "
            txt += f"Janela {st.session_state.get(f'jae_{kb}')}. "
            txt += f"Elétrica com {st.session_state.get(f'tq_{kb}')} tomadas (espelhos {st.session_state.get(f'tep_{kb}')}) e {st.session_state.get(f'iq_{kb}')} interruptores. "
            txt += f"Iluminação tipo {st.session_state.get(f'lti_{kb}')} {st.session_state.get(f'lst_{kb}')}. "
            
            if st.session_state.get(f'ra_{kb}'): txt += "Ralo presente em bom estado. "
            
            p = doc.add_paragraph(txt)
            if st.session_state.get(f'ob_{kb}'):
                doc.add_paragraph(f"OBSERVAÇÕES: {st.session_state.get(f'ob_{kb}')}")

            # Organização das Fotos 2x2
            fotos_locais = []
            for f_key in [f"fp_{kb}", f"fpa_{kb}", f"fab_{kb}", f"fel_{kb}"]:
                if f_key in st.session_state.fotos_db:
                    fotos_locais.append(st.session_state.fotos_db[f_key])

            if fotos_locais:
                doc.add_paragraph("\nREGISTROS FOTOGRÁFICOS:")
                for j in range(0, len(fotos_locais), 2):
                    table = doc.add_table(rows=1, cols=2)
                    for idx, photo in enumerate(fotos_locais[j:j+2]):
                        img_stream = io.BytesIO(photo.getvalue())
                        cell = table.rows[0].cells[idx]
                        run = cell.paragraphs[0].add_run()
                        run.add_picture(img_stream, width=Inches(3.0))

        target = io.BytesIO()
        doc.save(target)
        doc_bytes = target.getvalue()

        # Salva no Histórico
        st.session_state.historico.insert(0, {"nome": st.session_state.info_geral['end'], "data_doc": doc_bytes})
        if len(st.session_state.historico) > 2: st.session_state.historico.pop()
        
        st.success("✅ Vistoria finalizada com sucesso!")
        st.download_button("📥 BAIXAR RELATÓRIO WORD", doc_bytes, f"vistoria_{st.session_state.info_geral['end']}.docx")
