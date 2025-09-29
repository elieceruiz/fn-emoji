import streamlit as st

st.set_page_config(page_title="Demo Toggle con Botón")

if "toggle" not in st.session_state:
    st.session_state.toggle = False

entrada = st.text_input("Escribe algo y presiona ENTER o pulsa el botón:")

# Acción con ENTER si escribiste algo
if entrada:
    st.session_state.toggle = not st.session_state.toggle

# Acción con botón aunque no escribas nada
if st.button("🔄 Alternar"):
    st.session_state.toggle = not st.session_state.toggle

# Emoji
if st.session_state.toggle:
    st.markdown("😃 **Activo**")
else:
    st.markdown("😴 **Inactivo**")

st.json({
    "valor_capturado": entrada,
    "toggle_actual": st.session_state.toggle
})