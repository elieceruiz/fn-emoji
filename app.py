import streamlit as st

st.set_page_config(page_title="Debug Teclas", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Input de texto
key = st.text_input("Escribe algo y presiona ENTER:")

# Debug
st.json({
    "valor_capturado": key,
    "toggle_actual": st.session_state.toggle
})

# Si se escribió algo y se dio enter
if key:
    st.session_state.toggle = not st.session_state.toggle
    st.session_state.key = ""  # reset
    st.rerun()

# Mostrar emoji
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")