import streamlit as st

st.set_page_config(page_title="Demo Toggle con Emoji")

# Inicializar estados
if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Input de texto
entrada = st.text_input("Escribe algo y presiona ENTER:")

# Si hay entrada, alternamos el toggle
if entrada:
    st.session_state.toggle = not st.session_state.toggle

# Mostrar emoji según el estado
if st.session_state.toggle:
    st.markdown("😃 **Activo**")
else:
    st.markdown("😴 **Inactivo**")

# Debug JSON
st.json({
    "valor_capturado": entrada,
    "toggle_actual": st.session_state.toggle
})