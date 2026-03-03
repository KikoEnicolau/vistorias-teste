import streamlit as st
from datetime import datetime

# --- 1. CONFIGURAÇÕES E ESTILO ---
st.set_page_config(page_title="Vistoria Master Pro", page_icon="🏢", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-header {
        background-color: #0f172a; padding: 20px; color: white;
        text-align: center; font-size: 1.8rem; font-weight: bold;
        border-radius: 0 0 15px 15px; margin-bottom: 30px;
    }
    .stDownloadButton button { width: 100%; background-color: #16a34a !important; color: white !important; }
    .streamlit-expanderHeader { background-color: white !important; font-weight: bold !important; border: 1px solid #e2e8f0 !important; }
    </style>
    <div class="main-header">🏢 Vistoria Master Pro</div>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZAÇÃO DO ESTADO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "identificacao"
if 'dados_vistoria' not in st.session_state: st.session_state.dados_vistoria = {}
if 'comodos_lista' not in st.session_state: st.session_state.comodos_lista = []

# OPÇÕES PADRONIZADAS
OPCOES_PISO = ["porcelanato", "de cerâmica", "vinílico", "laminado", "de madeira", "frio"]
OPCOES_ESTADO = ["em bom estado", "novo", "usado"]
OPCOES_AVARIAS = ["Não", "riscos", "manchas", "trincado", "furos", "mofo"]
CORES_TINTA = ["Branco", "Gelo", "Palha", "Cinza Platina", "Areia"]

# --- ETAPA 1: IDENTIFICAÇÃO ---
if st.session_state.etapa == "identificacao":
    st.subheader("📍 1. Dados da Unidade")
    tipo_res = st.selectbox("Tipo do Imóvel", ["Casa Térrea", "Sobrado", "Apartamento"])
    end = st.text_input("Endereço Completo")
    insp = st.text_input("Nome do Vistoriador")
    
    if st.button("Confirmar e Seguir ➡️"):
        if end and insp:
            st.session_state.dados_vistoria['info_geral'] = {
                "tipo": tipo_res, "endereco": end, "inspetor": insp, "data": datetime.now().strftime("%d/%m/%Y")
            }
            st.session_state.etapa = "composicao"
            st.rerun()

# --- ETAPA 2: COMPOSIÇÃO ---
elif st.session_state.etapa == "composicao":
    st.subheader("🏠 2. Composição do Imóvel")
    c1, c2 = st.columns(2)
    t_sala = c1.checkbox("Sala", value=True); t_coz = c1.checkbox("Cozinha", value=True)
    t_ban = c2.checkbox("Banheiro Social", value=True); t_lav = c2.checkbox("Lavanderia", value=True)
    
    st.write("---")
    q_dorm = st.number_input("Dormitórios (Simples)", 0, 10, 1)
    q_suit = st.number_input("Suítes", 0, 10, 0)

    if st.button("Ir para Detalhamento ➡️"):
        lista = []
        if t_sala: lista.append("Sala")
        if t_coz: lista.append("Cozinha")
        if t_ban: lista.append("Banheiro Social")
        if t_lav: lista.append("Lavanderia")
        for i in range(q_dorm): lista.append(f"Dormitório {i+1}")
        for i in range(q_suit):
            lista.append(f"Suíte {i+1}"); lista.append(f"Banheiro Suíte {i+1}")
        st.session_state.comodos_lista = lista
        st.session_state.etapa = "detalhamento"
        st.rerun()

# --- ETAPA 3: DETALHAMENTO ---
elif st.session_state.etapa == "detalhamento":
    st.info(f"📍 {st.session_state.dados_vistoria['info_geral']['endereco']}")
    
    abas = st.tabs(st.session_state.comodos_lista)

    for i, nome_comodo in enumerate(st.session_state.comodos_lista):
        with abas[i]:
            key_id = f"{nome_comodo}_{i}"
            
            # Inicializa o dicionário do cômodo se não existir
            if key_id not in st.session_state.dados_vistoria:
                st.session_state.dados_vistoria[key_id] = {}

            # --- PISO ---
            with st.expander("🏗️ Piso", expanded=False):
                c1, c2, c3 = st.columns(3)
                tp = c1.selectbox("Tipo de Piso", OPCOES_PISO, key=f"p_t_{key_id}")
                ep = c2.selectbox("Estado", OPCOES_ESTADO, key=f"p_e_{key_id}")
                ap = c3.selectbox("Avarias", OPCOES_AVARIAS, key=f"p_a_{key_id}")
                av_txt = f" com {ap}" if ap != "Não" else ""
                frase_piso = f"- Piso {tp} {ep}{av_txt}"
                st.session_state.dados_vistoria[key_id]['piso'] = frase_piso
                st.info(frase_piso)

            # --- RODAPÉ ---
            with st.expander("📐 Rodapé", expanded=False):
                tem_r = st.radio("Contém Rodapé?", ["sim", "não"], horizontal=True, key=f"r_c_{key_id}")
                if tem_r == "sim":
                    r1, r2, r3 = st.columns(3)
                    tipo_r = r1.selectbox("Tipo de Rodapé", OPCOES_PISO, key=f"r_t_{key_id}")
                    est_r = r2.selectbox("Estado", OPCOES_ESTADO, key=f"r_e_{key_id}")
                    av_r = r3.selectbox("Avarias", OPCOES_AVARIAS, key=f"r_a_{key_id}")
                    av_r_txt = f" com {av_r}" if av_r != "Não" else ""
                    frase_rodape = f"- Rodapé em piso {tipo_r} {est_r}{av_r_txt}"
                    st.session_state.dados_vistoria[key_id]['rodape'] = frase_rodape
                    st.info(frase_rodape)
                else:
                    st.session_state.dados_vistoria[key_id]['rodape'] = ""

            # --- PAREDES ---
            with st.expander("🧱 Paredes", expanded=False):
                tipo_pa = st.selectbox("Tipo de Parede", ["Alvenaria", "Azulejos"], key=f"pa_t_{key_id}")
                av_pa = st.selectbox("Avarias", OPCOES_AVARIAS, key=f"pa_a_{key_id}")
                av_pa_txt = f" com {av_pa}" if av_pa != "Não" else ""
                
                if tipo_pa == "Azulejos":
                    est_az = st.selectbox("Estado do Azulejo", ["nova", "usada"], key=f"pa_e_az_{key_id}")
                    frase_pa = f"- Paredes com azulejos ate o teto {est_az}{av_pa_txt}"
                else:
                    c1, c2 = st.columns(2)
                    cor_pa = c1.selectbox("Cor da Tinta", CORES_TINTA, key=f"pa_cor_{key_id}")
                    est_pintura = c2.selectbox("Estado da Pintura", ["nova", "usada"], key=f"pa_e_al_{key_id}")
                    frase_pa = f"- Paredes em alvenaria em bom estado, na cor {cor_pa.lower()} com pintura {est_pintura}{av_pa_txt}"
                st.session_state.dados_vistoria[key_id]['parede'] = frase_pa
                st.info(frase_pa)

            # --- TETO ---
            with st.expander("☁️ Teto", expanded=False):
                c1, c2, c3 = st.columns(3)
                cor_t = c1.selectbox("Cor do Teto", CORES_TINTA, key=f"t_cor_{key_id}")
                est_t = c2.selectbox("Estado da Pintura", ["nova", "usada"], key=f"t_est_{key_id}")
                av_t = c3.selectbox("Avarias", OPCOES_AVARIAS, key=f"t_av_{key_id}")
                tem_gesso = st.radio("Acabamento em gesso?", ["não", "sim"], horizontal=True, key=f"t_gesso_{key_id}")
                av_t_txt = f" com {av_t}" if av_t != "Não" else ""
                frase_teto = f"- Teto na cor {cor_t.lower()}, com pintura {est_t}{av_t_txt}"
                if tem_gesso == "sim":
                    est_g = st.selectbox("Estado do Gesso", ["nova", "usada"], key=f"t_g_est_{key_id}")
                    frase_teto += f", com acabamento em gesso {est_g}"
                st.session_state.dados_vistoria[key_id]['teto'] = frase_teto
                st.info(frase_teto)

           # --- PORTA ---
            with st.expander("🚪 Porta", expanded=False):
                tem_porta = st.radio("Este cômodo possui porta?", ["não", "sim"], horizontal=True, key=f"po_check_{key_id}")
                
                if tem_porta == "sim":
                    c1, c2, c3 = st.columns(3)
                    tipo_po = c1.selectbox("Material da Porta", ["madeira", "ferro", "alumínio"], key=f"po_t_{key_id}")
                    cor_po = c2.selectbox("Cor da Porta", CORES_TINTA, key=f"po_c_{key_id}")
                    est_po = c3.selectbox("Estado da Porta", ["novo", "usado", "em bom estado"], key=f"po_e_{key_id}")
                    
                    # FECHADURA
                    fec_po = st.radio("Possui fechadura e maçaneta?", ["sim", "não"], horizontal=True, key=f"po_f_{key_id}")
                    fec_txt = ", com fechadura e maçaneta" if fec_po == "sim" else ""

                    # VIDROS (Lógica de Singular/Plural)
                    tem_vi = st.radio("A porta possui vidros?", ["não", "sim"], horizontal=True, key=f"po_v_c_{key_id}")
                    vi_txt = ""
                    if tem_vi == "sim":
                        v1, v2, v3 = st.columns(3)
                        qtd_vi = v1.number_input("Qtd Vidros", 1, 20, 1, key=f"po_v_q_{key_id}")
                        est_vi = v2.selectbox("Estado Vidros", ["novo", "usado", "em bom estado"], key=f"po_v_e_{key_id}")
                        av_vi = v3.selectbox("Avarias Vidros", ["Não", "trincado", "quebrado", "faltando"], key=f"po_v_a_{key_id}")
                        
                        # Ajuste Singular/Plural
                        palavra_vidro = "vidro" if qtd_vi == 1 else "vidros"
                        palavra_estado = est_vi if qtd_vi == 1 else est_vi.replace("novo", "novos").replace("usado", "usados")
                        
                        qtd_vi_f = str(qtd_vi).zfill(2)
                        av_vi_txt = f" {av_vi}" if av_vi != "Não" else ""
                        vi_txt = f", {qtd_vi_f} {palavra_vidro} {palavra_estado}{av_vi_txt}"

                    # BATENTE
                    tem_ba = st.radio("Possui batente?", ["não", "sim"], horizontal=True, key=f"po_b_c_{key_id}")
                    ba_txt = ""
                    if tem_ba == "sim":
                        b1, b2 = st.columns(2)
                        tipo_ba = b1.selectbox("Material do Batente", ["madeira", "ferro", "alumínio"], key=f"po_b_t_{key_id}")
                        est_ba = b2.selectbox("Estado do Batente", ["novo", "usado", "em bom estado"], key=f"po_b_e_{key_id}")
                        ba_txt = f", com batente de {tipo_ba} {est_ba}"

                    # Escrita Final da Porta com a Cor
                    frase_porta = f"- Porta de {tipo_po} na cor {cor_po.lower()} {est_po}{fec_txt}{vi_txt}{ba_txt}"
                    st.session_state.dados_vistoria[key_id]['porta'] = frase_porta
                    st.info(frase_porta)
                else:
                    st.session_state.dados_vistoria[key_id]['porta'] = ""

            # --- ILUMINAÇÃO ---
            with st.expander("💡 Iluminação", expanded=False):
                # Inicializa a lista de iluminação no estado do cômodo se não existir
                if 'iluminacao_itens' not in st.session_state.dados_vistoria[key_id]:
                    st.session_state.dados_vistoria[key_id]['iluminacao_itens'] = []

                # Form de entrada para novos itens
                c1, c2 = st.columns(2)
                tipo_il = c1.selectbox("Tipo", ["Spot", "Lustre", "Luminária", "Lâmpada dicroica"], key=f"il_t_{key_id}")
                
                # Só mostra material se não for dicroica
                material_il = ""
                if tipo_il != "Lâmpada dicroica":
                    material_il = c2.selectbox("Material", ["plástico", "ferro", "vidro"], key=f"il_m_{key_id}")
                
                c3, c4 = st.columns(2)
                qtd_il = c3.number_input("Quantidade", 1, 50, 1, key=f"il_q_{key_id}")
                est_il = c4.selectbox("Estado", ["novo", "usado", "em bom estado"], key=f"il_e_{key_id}")

                if st.button("➕ Adicionar outro", key=f"il_btn_{key_id}"):
                    # Lógica de Singular/Plural
                    nome_item = tipo_il.lower()
                    if qtd_il > 1:
                        if nome_item == "spot": nome_item = "spots"
                        elif nome_item == "lustre": nome_item = "lustres"
                        elif nome_item == "luminária": nome_item = "luminárias"
                        elif nome_item == "lâmpada dicroica": nome_item = "lâmpadas dicroicas"
                    
                    qtd_f = str(qtd_il).zfill(2)
                    mat_txt = f" de {material_il}" if material_il else ""
                    nova_frase = f"{qtd_f} {nome_item}{mat_txt} {est_il}"
                    
                    st.session_state.dados_vistoria[key_id]['iluminacao_itens'].append(nova_frase)

                # Exibe e limpa os itens adicionados
                itens_salvos = st.session_state.dados_vistoria[key_id].get('iluminacao_itens', [])
                if itens_salvos:
                    st.write("---")
                    for idx, item in enumerate(itens_salvos):
                        st.write(f"✔️ {item}")
                    
                    if st.button("🗑️ Limpar Iluminação", key=f"il_limp_{key_id}"):
                        st.session_state.dados_vistoria[key_id]['iluminacao_itens'] = []
                        st.rerun()

                # Monta a frase final para o relatório
                if itens_salvos:
                    frase_final_il = "- Iluminação: " + ", ".join(itens_salvos)
                    st.session_state.dados_vistoria[key_id]['iluminacao'] = frase_final_il
                else:
                    st.session_state.dados_vistoria[key_id]['iluminacao'] = ""

    # --- GERAÇÃO DO TEXTO FINAL PARA DOWNLOAD ---
    relatorio_final = f"LAUDO DE VISTORIA\nEndereço: {st.session_state.dados_vistoria['info_geral']['endereco']}\n\n"
    for kid in st.session_state.comodos_lista:
        # Encontra a chave correta no dicionário de dados
        idx = st.session_state.comodos_lista.index(kid)
        chave_busca = f"{kid}_{idx}"
        if chave_busca in st.session_state.dados_vistoria:
            dados_comodo = st.session_state.dados_vistoria[chave_busca]
            relatorio_final += f"[{kid.upper()}]\n"
            relatorio_final += dados_comodo.get('piso', '') + "\n"
            if dados_comodo.get('rodape'): relatorio_final += dados_comodo['rodape'] + "\n"
            relatorio_final += dados_comodo.get('parede', '') + "\n"
            relatorio_final += dados_comodo.get('teto', '') + "\n\n"
            relatorio_final += dados_comodo.get('porta', '') + "\n"
            relatorio_final += dados_comodo.get('iluminacao', '') + "\n"

    st.divider()
    st.download_button("📥 BAIXAR VISTORIA (.txt)", relatorio_final, file_name=f"Vistoria_{datetime.now().strftime('%Y%m%d')}.txt")
