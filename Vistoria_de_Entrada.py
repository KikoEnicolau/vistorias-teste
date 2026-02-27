import streamlit as st

# Configuração da página
st.set_page_config(page_title="Vistoria Técnica Pro", page_icon="🏠", layout="centered")

# --- LISTAS DE OPÇÕES ATUALIZADAS ---
OPCOES_ESTADO = ["Bom estado", "Novo", "Usado"]
OPCOES_CORES = ["Branca", "Gelo", "Cinza", "Bege", "Preta", "Marrom", "Amadeirada", "Off-white", "Natural"]

# Rodapé agora tem as mesmas opções do piso (sem o "mesmo material")
OPCOES_PISO_MAT = ["Frio", "Cerâmico", "Porcelanato", "Laminado", "Vinílico", "Ardósia", "Taco/Madeira"]
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
    titulo = f"📍 {nome_exibicao.upper()}" if not eh_sacada else f"🌅 SACADA DO(A) {nome_exibicao.upper()}"
    
    with st.expander(titulo, expanded=True):
        texto_acumulado = ""

        # --- PISO E RODAPÉ ---
        incluir_piso = st.checkbox("Incluir Piso/Rodapé?", value=False, key=f"inc_piso_{id_chave}")
        if incluir_piso:
            st.markdown("#### 1. Piso e Rodapé")
            c1, c2, c3 = st.columns(3)
            p_mat = c1.selectbox("Material Piso", OPCOES_PISO_MAT, key=f"p_mat_s_{id_chave}")
            p_cor = c2.selectbox("Cor Piso", OPCOES_CORES, key=f"p_cor_s_{id_chave}")
            p_est = c3.selectbox("Estado Piso", OPCOES_ESTADO, key=f"p_est_s_{id_chave}")
            
            st.write("Rodapé:")
            r1, r2, r3 = st.columns(3)
            roda_mat = r1.selectbox("Material Rodapé", OPCOES_RODAPE_MAT, key=f"r_mat_s_{id_chave}")
            roda_cor = r2.selectbox("Cor Rodapé", OPCOES_CORES, key=f"r_cor_s_{id_chave}")
            roda_est = r3.selectbox("Estado Rodapé", OPCOES_ESTADO, key=f"r_est_s_{id_chave}")
            
            p_obs = st.text_input("Obs. Piso/Rodapé", key=f"p_obs_i_{id_chave}")
            
            # Formatação do estado para Piso/Rodapé
            def fmt_est_piso(estado):
                if estado == "Bom estado": return "em bom estado"
                return estado.lower()

            txt_piso = f"- PISO: {p_mat} na cor {p_cor.lower()}, {fmt_est_piso(p_est)}."
            txt_rodape = f" RODAPÉ: {roda_mat} na cor {roda_cor.lower()}, {fmt_est_piso(roda_est)}."
            texto_acumulado += f"{txt_piso}{txt_rodape} {p_obs}\n"

        # --- PAREDES E TETO ---
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
                if est_txt == "bom estado":
                    return f"Cor {cor.lower()}, em bom estado"
                return f"Cor {cor.lower()}, com pintura {est_txt}"

            texto_acumulado += f"- PAREDES: {formatar_pintura(par_cor, par_est)}. TETO: {formatar_pintura(tet_cor, tet_est)}.\n"

        # --- PORTAS ---
        incluir_porta = st.checkbox("Incluir Porta/Batente?", value=False, key=f"inc_porta_{id_chave}")
        if incluir_porta:
            st.markdown("---")
            st.markdown("#### 3. Porta e Batente")
            cp1, cp2, cp3, cp4 = st.columns(4)
            por_mat = cp1.selectbox("Material", ["Madeira", "Alumínio", "Ferro"], key=f"p_mat_p_s_{id_chave}")
            por_cor = cp2.selectbox("Cor", OPCOES_CORES, key=f"p_cor_p_s_{id_chave}")
            por_est = cp3.selectbox("Estado", OPCOES_ESTADO, key=f"p_est_p_s_{id_chave}")
            fec_est = cp4.selectbox("Maçaneta", ["em bom estado"], key=f"fec_s_{id_chave}")
            
            po_status = f"em {por_est.lower()}" if por_est == "Bom estado" else f"com pintura {por_est.lower().replace('novo', 'nova').replace('usado', 'usada')}"
            texto_acumulado += f"- PORTA: {por_mat} na cor {por_cor.lower()}, {po_status}. Maçaneta {fec_est.lower()}.\n"

        # --- JANELAS ---
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
            
            j_status = f"em {jan_est.lower()}" if jan_est == "Bom estado" else jan_est.lower()
            v_status = f"em {vid_est_geral.lower()}" if vid_est_geral == "Bom estado" else vid_est_geral.lower()
            
            # Se for 1 vidro, escreve no singular. Se for mais, troca 'novo' por 'novos', etc.
            if q_vidros == 1:
                txt_vidros_estado = f"01 vidro {v_status}"
            else:
                # Usamos o .replace para colocar o 's' no final das palavras
                v_status_plural = v_status.replace("novo", "novos").replace("usado", "usados")
                txt_vidros_estado = f"{q_vidros:02} vidros {v_status_plural}"

            if tem_avaria == "Sim":
                vid_ava = st.selectbox("Avaria:", ["Trincado", "Quebrado", "Faltando"], key=f"vid_ava_sel_{id_chave}")
                # Se for mais de 1 vidro, coloca um 's' na avaria
                avaria_texto = vid_ava.lower() if q_vidros == 1 else vid_ava.lower() + "s"
                txt_vidros_estado = f"{q_vidros:02} vidros {avaria_texto}"

            texto_acumulado += f"- JANELA: {jan_mat} {j_status} ({q_trincos:02} trincos). {txt_vidros_estado}.\n"

        # --- ELÉTRICA ---
        incluir_eletrica = st.checkbox("Incluir Elétrica?", value=False, key=f"inc_ele_{id_chave}")
        if incluir_eletrica:
            st.markdown("---")
            st.markdown("#### 5. Elétrica")
            ce1, ce2, ce3 = st.columns(3)
            q_tom = ce1.number_input("Qtd Tomadas", 0, 50, key=f"q_tom_n_{id_chave}")
            q_int = ce2.number_input("Qtd Interruptores", 0, 50, key=f"q_int_n_{id_chave}")
            ele_est = ce3.selectbox("Estado Placas", OPCOES_ESTADO, key=f"ele_est_s_{id_chave}")
            
            e_status = f"em {ele_est.lower()}" if ele_est == "Bom estado" else ele_est.lower()
            # Adicionado "de plástico" conforme solicitado
            texto_acumulado += f"- ELÉTRICA: {q_tom} tomadas e {q_int} interruptores de plástico {e_status}.\n"

        # --- ILUMINAÇÃO ---
        incluir_ilum = st.checkbox("Incluir Iluminação?", value=False, key=f"inc_ilum_{id_chave}")
        if incluir_ilum:
            st.markdown("---")
            st.markdown("#### 6. Iluminação")
            ilu_tipo = st.multiselect("Tipo", ["Lâmpada simples", "Spot de LED", "Spot de Plástico", "Luminária", "Plafon"], default=["Lâmpada simples"], key=f"ilu_t_m_{id_chave}")
            
            ci1, ci2, ci3, ci4 = st.columns(4)
            q_total = ci1.number_input("Qtd Total", 0, 100, key=f"q_tot_n_{id_chave}")
            ilu_est = ci2.selectbox("Estado", OPCOES_ESTADO + ["Sem teste"], key=f"ilu_e_s_{id_chave}")
            q_func = ci3.number_input("Funcionando", 0, 100, key=f"q_fun_n_{id_chave}")
            q_queim = ci4.number_input("Queimadas", 0, 100, key=f"q_queim_n_{id_chave}")
            
            tipos_ajustados = []
            for t in ilu_tipo:
                nome = t
                if q_total > 1:
                    if "Spot" in t: nome = t.replace("Spot", "Spots")
                    if "Lâmpada" in t: nome = t.replace("Lâmpada", "Lâmpadas")
                    if "Luminária" in t: nome = t.replace("Luminária", "Luminárias")
                tipos_ajustados.append(nome.lower())

            i_status = f"em {ilu_est.lower()}" if ilu_est == "Bom estado" else ilu_est.lower()
            txt_ilum = f"- ILUMINAÇÃO: {q_total:02} {', '.join(tipos_ajustados)} {i_status}."
            if ilu_est.lower() != "sem teste":
                # Alterado de "Ok" para "Funcionando" conforme solicitado
                txt_ilum += " Todas funcionando." if q_queim == 0 else f" Funcionando: {q_func} / Queimada: {q_queim}."
            texto_acumulado += txt_ilum + "\n"

        # --- RALO ---
        if eh_sacada or any(x in nome_exibicao.lower() for x in ["cozinha", "banheiro", "serviço", "suíte"]):
            incluir_ralo = st.checkbox("Incluir Ralo?", value=False, key=f"inc_ralo_{id_chave}")
            if incluir_ralo:
                st.markdown("---")
                st.markdown("#### 7. Ralo")
                cr1, cr2 = st.columns(2)
                r_mat = cr1.selectbox("Material Ralo", OPCOES_RALO_MAT, key=f"r_mat_s_ralo_{id_chave}")
                r_est = cr2.selectbox("Estado Ralo", OPCOES_ESTADO, key=f"r_est_s_ralo_{id_chave}")
                ra_status = f"em {r_est.lower()}" if r_est == "Bom estado" else r_est.lower()
                texto_acumulado += f"- RALO: {r_mat} {ra_status}.\n"

    prefixo = f"### SACADA DO(A) {nome_exibicao.upper()}" if eh_sacada else f"### {nome_exibicao.upper()}"
    return f"{prefixo}\n{texto_acumulado}\n"

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
    nome = f"Suíte {i+1}"
    relatorio_total += formulario_base(f"suite_{i+1}", nome)
    if st.checkbox(f"{nome} tem sacada?", key=f"chk_sac_s_{i}"):
        relatorio_total += formulario_base(f"sacada_s_{i+1}", nome, eh_sacada=True)

for item in outros:
    if item != "Sala":
        relatorio_total += formulario_base(item.lower().replace(" ", "_"), item)

st.header("📄 Relatório")
if relatorio_total:
    st.code(relatorio_total, language="markdown")
    st.download_button("📥 Baixar Vistoria", relatorio_total, "vistoria.txt")
