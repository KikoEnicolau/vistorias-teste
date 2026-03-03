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
                    frase_pa = f"- Paredes em alvenaria em bom estado, na cor {cor_pa.lower()} with pintura {est_pintura}{av_pa_txt}"
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
                    fec_po = st.radio("Possui fechadura e maçaneta?", ["sim", "não"], horizontal=True, key=f"po_f_{key_id}")
                    fec_txt = ", com fechadura e maçaneta" if fec_po == "sim" else ""
                    frase_porta = f"- Porta de {tipo_po} na cor {cor_po.lower()} {est_po}{fec_txt}"
                    st.session_state.dados_vistoria[key_id]['porta'] = frase_porta
                    st.info(frase_porta)
                else:
                    st.session_state.dados_vistoria[key_id]['porta'] = ""

            # --- ILUMINAÇÃO (SISTEMA DIRETO) ---
            with st.expander("💡 Iluminação", expanded=False):
                c1, c2 = st.columns(2)
                tipo_il = c1.selectbox("Tipo", ["Spot", "Lustre", "Luminária", "Lâmpada dicroica"], key=f"il_t_{key_id}")
                material_il = ""
                if tipo_il != "Lâmpada dicroica":
                    material_il = c2.selectbox("Material", ["plástico", "ferro", "vidro"], key=f"il_m_{key_id}")
                
                c3, c4 = st.columns(2)
                qtd_il = c3.number_input("Quantidade de itens", 1, 50, 1, key=f"il_q_{key_id}")
                est_il = c4.selectbox("Estado do item", OPCOES_ESTADO, key=f"il_e_{key_id}")

                st.write("**Lâmpadas:**")
                tem_lampada = st.radio("Possui lâmpada?", ["sim", "não"], horizontal=True, key=f"il_l_c_{key_id}")
                
                lamp_txt = ""
                if tem_lampada == "não":
                    lamp_txt = ", sem lâmpada"
                else:
                    l1, l2 = st.columns(2)
                    qtd_f = l1.number_input("Qtd Funcionando", 0, 50, 0, key=f"il_l_f_{key_id}")
                    qtd_q = l2.number_input("Qtd Queimadas", 0, 50, 0, key=f"il_l_q_{key_id}")
                    
                    partes = []
                    if qtd_f > 0: partes.append(f"{str(qtd_f).zfill(2)} {'lâmpada funcionando' if qtd_f == 1 else 'lâmpadas funcionando'}")
                    if qtd_q > 0: partes.append(f"{str(qtd_q).zfill(2)} {'lâmpada queimada' if qtd_q == 1 else 'lâmpadas queimadas'}")
                    lamp_txt = ", sendo " + " e ".join(partes) if partes else ", com lâmpadas (não testadas)"

                # Formatação Singular/Plural
                nome_formatado = tipo_il.lower()
                if qtd_il > 1:
                    nome_formatado = nome_formatado.replace("spot", "spots").replace("lustre", "lustres").replace("luminária", "luminárias").replace("lâmpada dicroica", "lâmpadas dicroicas")
                
                mat_txt = f" de {material_il}" if material_il else ""
                frase_iluminacao = f"- Iluminação: {str(qtd_il).zfill(2)} {nome_formatado}{mat_txt} {est_il}{lamp_txt}"
                
                # Salvamento Automático (sem botão)
                st.session_state.dados_vistoria[key_id]['iluminacao'] = frase_iluminacao
                st.info(frase_iluminacao)

    # --- ÁREA DE DOWNLOAD ---
    st.divider()

    def montar_relatorio():
        info = st.session_state.dados_vistoria.get('info_geral', {'endereco': '', 'inspetor': '', 'data': ''})
        texto = f"LAUDO DE VISTORIA\nEndereço: {info['endereco']}\nVistoriador: {info['inspetor']}\nData: {info['data']}\n\n"
        
        for i, kid in enumerate(st.session_state.comodos_lista):
            chave_busca = f"{kid}_{i}"
            if chave_busca in st.session_state.dados_vistoria:
                dados = st.session_state.dados_vistoria[chave_busca]
                texto += f"[{kid.upper()}]\n"
                for campo in ['piso', 'rodape', 'parede', 'teto', 'porta', 'iluminacao']:
                    valor = dados.get(campo)
                    if valor: texto += f"{valor}\n"
                texto += "\n"
        return texto

    st.download_button(
        label="📥 BAIXAR VISTORIA (.txt)",
        data=montar_relatorio(),
        file_name=f"Vistoria_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

    if st.sidebar.button("⬅️ Reiniciar"):
        st.session_state.etapa = "identificacao"
        st.session_state.dados_vistoria = {}
        st.rerun()
