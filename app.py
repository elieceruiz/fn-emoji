import streamlit as st

st.set_page_config(page_title="Toggle Emoji", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Campo para capturar la tecla
key = st.text_input("Presiona ENTER aquí", "")

# Cuando el usuario presiona Enter, se dispara
if key != "":
    st.session_state.toggle = not st.session_state.toggle
    st.session_state.key = ""  # limpiar
    st.rerun()

# Mostrar estado
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")