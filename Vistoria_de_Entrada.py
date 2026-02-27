import streamlit as st

# Configuração da página
st.set_page_config(page_title="Vistoria Técnica Pro", page_icon="🏠", layout="centered")

# --- LISTAS DE OPÇÕES ---
OPCOES_ESTADO = ["Bom estado", "Novo", "Usado"]
OPCOES_CORES = ["Branca", "Gelo", "Cinza", "Bege", "Preta", "Marrom", "Amadeirada", "Off-white", "Natural"]

OPCOES_PISO_MAT = ["Frio", "Cerâmico", "Porcelanato", "Laminado", "Vinílico", "Ardósia", "Taco/Mad."]
OPCOES_RODAPE_MAT = OPCOES_PISO_MAT + ["Madeira/MDF", "Poliuretano", "PVC", "Poliestireno"]
OPCOES_RALO_MAT = ["Plástico", "Inox", "Ferro"]

# --- ESTILIZAÇÃO ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #2e7d32; color: white; }
    div[data-testid="stExpander"] { border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px; }
    h4 { color: #2e7d32; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

def formulario_base(id_chave, nome_exibicao, eh_sacada=False):
    # Lógica de título
    if eh_sacada:
        if "sala" in nome_exibicao.lower(): titulo_secao = "Sacada da sala"
        elif "quarto" in nome_exibicao.lower(): titulo_secao = f"Sacada do {nome_exibicao.lower()}"
        elif "suíte" in nome_exibicao.lower(): titulo_secao = f"Sacada da {nome_exibicao.lower()}"
        else: titulo_secao = f"Sacada do(a) {nome_exibicao.lower()}"
    else:
        titulo_secao = nome_exibicao.upper()
    
    with st.expander(f"📍 {titulo_secao.upper()}", expanded=True):
        texto_acumulado = ""

        # --- 1. PISO E RODAPÉ ---
        incluir_piso = st.checkbox("Incluir Piso/Rodapé?", value=False, key=f"inc_piso_{id_chave}")
        if incluir_piso:
            st.markdown("#### 1. Piso e Rodapé")
            c1, c2, c3 = st.columns(3)
            p_mat = c1.selectbox("Material Piso", OPCOES_PISO_MAT, key=f"p_mat_s_{id_chave}")
            p_cor = c2.selectbox("Cor Piso", OPCOES_CORES, key=f"p_cor_s_{id_chave}")
            p_est = c3.selectbox("Estado Piso", OPCOES_ESTADO, key=f"p_est_s_{id_chave}")
            p_obs = st.text_input("Obs. Piso", key=f"p_obs_i_{id_chave}")
            
            def fmt_est(estado):
                return "em bom estado" if estado == "Bom estado" else estado.lower()

            txt_piso = f"- PISO: {p_mat} na cor {p_cor.lower()}, {fmt_est(p_est)}."
            
            # Lógica Condicional: APENAS Cozinha, Banheiro Social e Banheiro da Suíte
            # Verificamos se é banheiro ou cozinha, mas ignoramos se for apenas a Suíte (quarto)
            nome_lc = nome_exibicao.lower()
            eh_area_sem_rodape_padrao = "cozinha" in nome_lc or "banheiro" in nome_lc or "serviço" in nome_lc
            
            mostrar_rodape = True
            if eh_area_sem_rodape_padrao:
                mostrar_rodape = st.checkbox("Tem rodapé?", value=False, key=f"tem_roda_{id_chave}")
            
            txt_rodape = ""
            if mostrar_rodape:
                st.write("Rodapé:")
                r1, r2, r3 = st.columns(3)
                roda_mat = r1.selectbox("Material Rodapé", OPCOES_RODAPE_MAT, key=f"r_mat_s_{id_chave}")
                roda_cor = r2.selectbox("Cor Rodapé", OPCOES_CORES, key=f"r_cor_s_{id_chave}")
                roda_est = r3.selectbox("Estado Rodapé", OPCOES_ESTADO, key=f"r_est_s_{id_chave}")
                txt_rodape = f" RODAPÉ: {roda_mat} na cor {roda_cor.lower()}, {fmt_est(roda_est)}."
            
            texto_acumulado += f"{txt_piso}{txt_rodape} {p_obs}\n"

        # --- 2. PAREDES E TETO ---
        incluir_par = st.checkbox("Incluir Paredes/Teto?", value=False, key=f"inc_par_{id_chave}")
        if incluir_par:
            st.markdown("---")
            st.markdown("#### 2. Paredes e Teto")
            c4, c5, c6, c7 = st.columns(4)
            par_cor = c4.selectbox("Cor Paredes", OPCOES_CORES, key=f"par_cor_s_{id_chave}")
            par_est = c5.selectbox("Estado Paredes", OPCOES_ESTADO, key=f"par_est_s_{id_chave}")
            tet_cor = c6.selectbox("Cor Teto", OPCOES_CORES, key=f"tet_cor_s_{id_chave}")
            tet_est = c7.selectbox("Estado Teto", OPCOES_ESTADO, key=f"tet_est_s_{id_chave}")
            
            def formatar_pintura(cor, estado):
                est_txt = estado.lower().replace("novo", "nova").replace("usado", "usada")
                if "bom estado" in est_txt: return f"Cor {cor.lower()}, em bom estado"
                return f"Cor {cor.lower()}, com pintura {est_txt}"

            texto_acumulado += f"- PAREDES: {formatar_pintura(par_cor, par_est)}. TETO: {formatar_pintura(tet_cor, tet_est)}.\n"

        # --- 3. PORTAS ---
        incluir_porta = st.checkbox("Incluir Porta/Batente?", value=False, key=f"inc_porta_{id_chave}")
        if incluir_porta:
            st.markdown("---")
            st.markdown("#### 3. Porta e Batente")
            cp1, cp2, cp3, cp4 = st.columns(4)
            por_mat = cp1.selectbox("Material", ["Madeira", "Alumínio Branco", "Alumínio Preto", "Ferro", "PVC"], key=f"p_mat_p_s_{id_chave}")
            por_cor = cp2.selectbox("Cor", OPCOES_CORES, key=f"p_cor_p_s_{id_chave}")
            por_est = cp3.selectbox("Estado", OPCOES_ESTADO, key=f"p_est_p_s_{id_chave}")
            fec_est = cp4.selectbox("Maçaneta", ["Funcionando", "Com folga", "Sem chave", "Oxidada"], key=f"fec_s_{id_chave}")
            
            po_status = f"em {por_est.lower()}" if por_est == "Bom estado" else f"com pintura {por_est.lower().replace('novo', 'nova').replace('usado', 'usada')}"
            texto_acumulado += f"- PORTA: {por_mat} na cor {por_cor.lower()}, {po_status}. Maçaneta {fec_est.lower()}.\n"

        # --- 4. JANELAS ---
        incluir_janela = st.checkbox("Incluir Janelas?", value=False, key=f"inc_janela_{id_chave}")
        if incluir_janela:
            st.markdown("---")
            st.markdown("#### 4. Janelas e Vidros")
            cj1, cj2, cj3 = st.columns(3)
            jan_mat = cj1.selectbox("Material Janela", ["Alumínio", "Madeira", "Ferro"], key=f"j_mat_s_{id_chave}")
            jan_est = cj2.selectbox("Estado Janela", OPCOES_ESTADO, key=f"jan_est_s_{id_chave}")
            vid_est_geral = cj3.selectbox("Estado Vidros", OPCOES_ESTADO, key=f"vid_est_s_{id_chave}")
            
            cj4, cj5, cj6 = st.columns(3)
            q_vidros = cj4.number_input("Qtd Vidros", 0, 20, value=1, key=f"q_vid_{id_chave}")
            q_trincos = cj5.number_input("Qtd Trincos", 0, 10, value=1, key=f"q_tri_{id_chave}")
            tem_avaria = cj6.radio("Avarias no vidro?", ["Não", "Sim"], key=f"vid_radio_{id_chave}")
            
            v_status_base = vid_est_geral.lower() if vid_est_geral != "Bom estado" else "em bom estado"
            txt_vidros = f"{q_vidros:02} vidro(s) {v_status_base.replace('novo', 'novos').replace('usado', 'usados')}"

            texto_acumulado += f"- JANELA: {jan_mat} {jan_est.lower()} com {q_trincos} trincos e {txt_vidros}.\n"

        # --- 5. ILUMINAÇÃO ---
        incluir_ilum = st.checkbox("Incluir Iluminação?", value=False, key=f"inc_ilum_{id_chave}")
        if incluir_ilum:
            st.markdown("---")
            st.markdown("#### 5. Iluminação")
            ci1, ci2, ci3 = st.columns(3)
            tipo_ilu = ci1.selectbox("Tipo", ["Spot de plástico", "Plafon de vidro", "Luminária de vidro", "Luminária led", "Lâmpada dicroica"], key=f"t_ilu_{id_chave}")
            q_tipo = ci2.number_input(f"Qtd total de {tipo_ilu.lower()}s", 0, 100, value=1, key=f"q_t_ilu_{id_chave}")
            est_tipo = ci3.selectbox("Estado estrutura", OPCOES_ESTADO, key=f"e_t_ilu_{id_chave}")

            st.write("Sobre as Lâmpadas:")
            ci4, ci5, ci6 = st.columns(3)
            q_lamps = ci4.number_input("Qtd total de Lâmpadas", 0, 100, value=1, key=f"q_l_{id_chave}")
            est_lamps = ci5.selectbox("Estado Lâmpadas", OPCOES_ESTADO, key=f"e_l_{id_chave}")
            q_vazios = ci6.number_input("Qtd spots sem lâmpada", 0, 100, value=0, key=f"q_v_{id_chave}")

            ci7, ci8 = st.columns(2)
            q_func = ci7.number_input("Funcionando", 0, 100, value=q_lamps, key=f"q_f_{id_chave}")
            q_queim = ci8.number_input("Queimada", 0, 100, value=0, key=f"q_q_{id_chave}")

            nome_tipo = tipo_ilu.lower() if q_tipo == 1 else f"{tipo_ilu.lower()}s"
            status_estru = fmt_est(est_tipo)
            txt_base = f"- ILUMINAÇÃO: {q_tipo:02} {nome_tipo} {status_estru}"

            status_l = fmt_est(est_lamps)
            if q_lamps == 0: txt_l = ", sem lâmpadas"
            else: txt_l = f" com {q_lamps:02} lâmpada(s) {status_l}"

            txt_v = f", sendo {q_vazios:02} sem lâmpadas" if q_vazios > 0 else ""
            txt_f = ""
            if q_lamps > 0:
                txt_f = ". Todas funcionando." if q_queim == 0 else f". Funcionando: {q_func:02} / Queimada: {q_queim:02}."

            texto_acumulado += f"{txt_base}{txt_l}{txt_v}{txt_f}\n"

        # --- 6. ELÉTRICA ---
        incluir_eletrica = st.checkbox("Incluir Elétrica?", value=False, key=f"inc_ele_{id_chave}")
        if incluir_eletrica:
            st.markdown("---")
            st.markdown("#### 6. Elétrica")
            ce1, ce2, ce3 = st.columns(3)
            q_tom = ce1.number_input("Qtd Tomadas", 0, 50, key=f"q_tom_{id_chave}")
            q_int = ce2.number_input("Qtd Interruptores", 0, 50, key=f"q_int_{id_chave}")
            ele_est = ce3.selectbox("Estado Placas", OPCOES_ESTADO, key=f"ele_est_{id_chave}")
            texto_acumulado += f"- ELÉTRICA: {q_tom} tomadas e {q_int} interruptores de plástico {fmt_est(ele_est)}.\n"

            incluir_caixa = st.checkbox("Incluir Caixa de Disjuntores?", value=False, key=f"inc_caixa_{id_chave}")
            if incluir_caixa:
                cd1, cd2, cd3 = st.columns(3)
                caixa_mat = cd1.selectbox("Material da Caixa", ["Plástico", "Ferro", "Madeira"], key=f"caixa_mat_{id_chave}")
                caixa_portas = cd2.number_input("Qtd portas", 1, 10, value=1, key=f"caixa_portas_{id_chave}")
                if caixa_mat == "Ferro":
                    enf = cd3.radio("Enferrujada?", ["Não", "Sim"], key=f"caixa_enf_{id_chave}")
                    st_c = "em bom estado" if enf == "Não" else "enferrujada"
                elif caixa_mat == "Madeira":
                    c_cor = cd3.selectbox("Cor Madeira", OPCOES_CORES, key=f"caixa_cor_{id_chave}")
                    c_pint = st.radio("Pintura", ["Nova", "Usada"], key=f"caixa_pint_{id_chave}", horizontal=True)
                    st_c = f"na cor {c_cor.lower()}, pintura {c_pint.lower()}"
                else: 
                    est_p = cd3.selectbox("Estado", OPCOES_ESTADO, key=f"caixa_est_p_{id_chave}")
                    st_c = fmt_est(est_p)
                texto_acumulado += f"- CAIXA DE DISJUNTORES: {caixa_mat} com {caixa_portas:02} porta(s) {st_c}.\n"

        # --- 7. RALO ---
        if any(x in nome_exibicao.lower() for x in ["cozinha", "banheiro", "serviço", "suíte", "sacada"]) or eh_sacada:
            incluir_ralo = st.checkbox("Incluir Ralo?", value=False, key=f"inc_ralo_{id_chave}")
            if incluir_ralo:
                st.markdown("---")
                st.markdown("#### 7. Ralo")
                cr1, cr2 = st.columns(2)
                r_mat = cr1.selectbox("Material Ralo", OPCOES_RALO_MAT, key=f"r_mat_{id_chave}")
                r_est = cr2.selectbox("Estado Ralo", OPCOES_ESTADO, key=f"r_est_{id_chave}")
                texto_acumulado += f"- RALO: {r_mat} {fmt_est(r_est)}.\n"

    return f"### {titulo_secao.upper()}\n{texto_acumulado}\n"

# --- INTERFACE PRINCIPAL ---
st.title("📋 Vistoria Pro")
col1, col2 = st.columns(2)
q_quartos = col1.number_input("Quartos", 0, 10, value=1)
q_suites = col2.number_input("Suítes", 0, 10, value=0)
outros = st.multiselect("Áreas:", ["Sala", "Cozinha", "Banheiro Social", "Área de Serviço", "Garagem"], default=["Sala", "Cozinha"])

relatorio_total = ""

if "Sala" in outros:
    relatorio_total += formulario_base("sala_0", "Sala")
    if st.checkbox("Sala tem sacada?", key="chk_sac_sala"):
        relatorio_total += formulario_base("sacada_sala", "Sala", eh_sacada=True)

for i in range(int(q_quartos)):
    nome = f"Quarto {i+1}"
    relatorio_total += formulario_base(f"quarto_{i+1}", nome)
    if st.checkbox(f"{nome} tem sacada?", key=f"chk_sac_q_{i}"):
        relatorio_total += formulario_base(f"sacada_q_{i+1}", nome, eh_sacada=True)

for i in range(int(q_suites)):
    nome_quarto = f"Suíte {i+1}"
    nome_banheiro = f"Banheiro da Suíte {i+1}"
    
    # 1. Formulário do Quarto da Suíte
    relatorio_total += formulario_base(f"suite_q_{i+1}", nome_quarto)
    if st.checkbox(f"{nome_quarto} tem sacada?", key=f"chk_sac_s_{i}"):
        relatorio_total += formulario_base(f"sacada_s_{i+1}", nome_quarto, eh_sacada=True)
    
    # 2. Formulário do Banheiro da Suíte (Onde o rodapé será opcional)
    relatorio_total += formulario_base(f"suite_b_{i+1}", nome_banheiro)

for item in outros:
    if item != "Sala":
        relatorio_total += formulario_base(item.lower().replace(" ", "_"), item)

st.header("📄 Relatório Final")
if relatorio_total:
    st.code(relatorio_total, language="markdown")
    st.download_button("📥 Baixar Vistoria", relatorio_total, "vistoria.txt")
