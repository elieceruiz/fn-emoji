# key_input_toggle.py
import streamlit as st

st.set_page_config(page_title="Key Input Toggle", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Campo de texto oculto
key = st.text_input("Presiona una tecla", key="key_input", label_visibility="collapsed")

# Cada vez que cambia, se procesa
if key:
    if key.lower() in ["delete", "shift", "enter"]:  # puedes ajustar la tecla
        st.session_state.toggle = not st.session_state.toggle
        st.session_state.key_input = ""  # limpiamos
        st.rerun()

# Mostrar estado
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")