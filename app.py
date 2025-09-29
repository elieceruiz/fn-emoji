import streamlit as st
from streamlit_keyup import keyup

st.set_page_config(page_title="Toggle con tecla", layout="centered")

# Estado inicial
if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Capturar tecla
key = keyup("Presiona una tecla")

# Si se presiona Enter, alternar estado
if key == "Enter":
    st.session_state.toggle = not st.session_state.toggle

# Mostrar estado
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")