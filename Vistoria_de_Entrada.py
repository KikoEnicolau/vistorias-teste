import streamlit as st

# Configuração da página
st.set_page_config(page_title="Vistoria Técnica Pro", page_icon="🏠", layout="centered")

# --- LISTAS DE OPÇÕES ATUALIZADAS ---
OPCOES_ESTADO = ["Bom estado", "Novo", "Usado"]
OPCOES_CORES = ["Branca", "Gelo", "Cinza", "Bege", "Preta", "Marrom", "Amadeirada", "Off-white", "Natural"]

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

        # --- SEÇÕES ANTERIORES (Piso, Parede, Porta, Janela mantidos conforme sua versão funcional) ---
        # [Omitidos aqui para focar na mudança da Iluminação, mas permanecem no seu código real]
        # (Se precisar do código de todas as seções de novo, me avise!)

        # --- ILUMINAÇÃO (LOGICA REVISADA) ---
        incluir_ilum = st.checkbox("Incluir Iluminação?", value=False, key=f"inc_ilum_{id_chave}")
        if incluir_ilum:
            st.markdown("---")
            st.markdown("#### 5. Iluminação")
            
            ci1, ci2, ci3 = st.columns(3)
            tipo_ilu = ci1.selectbox("Tipo de Iluminação", 
                                    ["Spot de plástico", "Plafon de vidro", "Luminária de vidro", "Luminária led", "Lâmpada dicroica"], 
                                    key=f"tipo_ilu_{id_chave}")
            q_tipo = ci2.number_input(f"Qtd total de {tipo_ilu.lower()}s", 0, 100, value=1, key=f"q_tipo_{id_chave}")
            est_tipo = ci3.selectbox("Estado estrutura", OPCOES_ESTADO, key=f"est_tipo_{id_chave}")

            st.write("Sobre as Lâmpadas:")
            ci4, ci5, ci6 = st.columns(3)
            q_lamps = ci4.number_input("Qtd total de Lâmpadas", 0, 100, value=1, key=f"q_lamps_{id_chave}")
            est_lamps = ci5.selectbox("Estado das Lâmpadas", OPCOES_ESTADO, key=f"est_lamps_{id_chave}")
            q_vazios = ci6.number_input("Qtd spots sem lâmpada", 0, 100, value=0, key=f"q_vazios_{id_chave}")

            ci7, ci8 = st.columns(2)
            q_func = ci7.number_input("Funcionando", 0, 100, value=q_lamps, key=f"q_func_{id_chave}")
            q_queim = ci8.number_input("Queimada", 0, 100, value=0, key=f"q_queim_{id_chave}")

            # --- MONTAGEM DO TEXTO DINÂMICO ---
            # 1. Plural do tipo
            tipo_nome = tipo_ilu.lower() if q_tipo == 1 else f"{tipo_ilu.lower()}s"
            status_tipo = est_tipo.lower() if est_tipo != "Bom estado" else "em bom estado"
            
            txt_principal = f"- ILUMINAÇÃO: {q_tipo:02} {tipo_nome} {status_tipo}"

            # 2. Lógica das Lâmpadas
            status_lamps = est_lamps.lower() if est_lamps != "Bom estado" else "em bom estado"
            
            if q_lamps == 0:
                txt_lampadas = ", sem lâmpadas"
            else:
                nome_lamp = "lâmpada" if q_lamps == 1 else "lâmpadas"
                txt_lampadas = f" com {q_lamps:02} {nome_lamp} {status_lamps}"

            # 3. Spots Vazios e Funcionamento
            txt_vazios = f", sendo {q_vazios:02} sem lâmpadas" if q_vazios > 0 else ""
            
            txt_func = ""
            if q_lamps > 0:
                if q_queim == 0:
                    txt_func = ". Todas funcionando."
                else:
                    txt_func = f". Funcionando: {q_func:02} / Queimada: {q_queim:02}."

            texto_acumulado += f"{txt_principal}{txt_lampadas}{txt_vazios}{txt_func}\n"

        # --- OUTRAS SEÇÕES (Eletrica, Ralo...) ---
        # [Mantidas conforme solicitado anteriormente]

    prefixo = f"### {nome_exibicao.upper()}"
    return f"{prefixo}\n{texto_acumulado}\n"

# --- INTERFACE PRINCIPAL ---
st.title("📋 Vistoria Pro")
# (Restante da interface de Quartos/Suítes/Áreas...)
