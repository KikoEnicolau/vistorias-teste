import streamlit as st

# --- ESTADOS E OPÇÕES (Padronizados para facilitar) ---
OPCOES_PISO = ["Porcelanato", "Cerâmica", "Vinílico", "Laminado", "Madeira", "Frio"]
OPCOES_ESTADO = ["em bom estado", "novo", "usado"]
OPCOES_AVARIAS = ["Não", "riscos", "manchas", "trincado"]

# --- ETAPA 3: DETALHAMENTO DA SALA ---
if st.session_state.etapa == "detalhe_sala":
    st.subheader("🛋️ Detalhamento: Sala")
    
    # --- SEÇÃO PISO ---
    st.markdown("#### 🏗️ Piso")
    with st.container():
        c1, c2, c3 = st.columns(3)
        tipo_piso = c1.selectbox("Tipo de Piso", OPCOES_PISO, key="sala_piso_tipo")
        estado_piso = c2.selectbox("Estado", OPCOES_ESTADO, key="sala_piso_estado")
        avaria_piso = c3.selectbox("Avarias", OPCOES_AVARIAS, key="sala_piso_avaria")
        
        # Gerando a frase do piso conforme sua regra
        if avaria_piso == "Não":
            frase_piso = f"- Piso {tipo_piso.lower()} {estado_piso}"
        else:
            frase_piso = f"- Piso {tipo_piso.lower()} {estado_piso} com {avaria_piso}"
        
        st.info(f"**Prévia da escrita:** {frase_piso}")

    st.write("---")

    # --- SEÇÃO RODAPÉ ---
    st.markdown("#### 📐 Rodapé")
    contem_rodape = st.radio("Contém Rodapé?", ["sim", "não"], horizontal=True, key="sala_roda_check")
    
    frase_rodape = "" # Começa vazio
    
    if contem_rodape == "sim":
        c1, c2, c3 = st.columns(3)
        tipo_roda = c1.selectbox("Tipo de Rodapé", OPCOES_PISO, key="sala_roda_tipo")
        estado_roda = c2.selectbox("Estado", OPCOES_ESTADO, key="sala_roda_estado")
        avaria_roda = c3.selectbox("Avarias", OPCOES_AVARIAS, key="sala_roda_avaria")
        
        if avaria_roda == "Não":
            frase_rodape = f"- Rodapé {tipo_roda.lower()} {estado_roda}"
        else:
            frase_rodape = f"- Rodapé {tipo_roda.lower()} {estado_roda} com {avaria_roda}"
            
        st.info(f"**Prévia da escrita:** {frase_rodape}")
    else:
        st.warning("Rodapé não será incluído no relatório.")

    # --- BOTÃO PARA SALVAR ---
    st.write("---")
    if st.button("Salvar Piso e Rodapé e Continuar ➡️"):
        # Armazenamos as frases prontas no banco de dados
        st.session_state.dados_vistoria['sala_piso_final'] = frase_piso
        st.session_state.dados_vistoria['sala_roda_final'] = frase_rodape
        # st.session_state.etapa = "detalhe_sala_paredes" # Próximo passo
        st.success("Dados da Sala salvos com sucesso!")

    if st.sidebar.button("⬅️ Voltar para Composição"):
        st.session_state.etapa = "composicao"
        st.rerun()
