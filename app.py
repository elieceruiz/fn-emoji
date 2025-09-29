# app.py
import streamlit as st
from my_key_listener import my_key_listener

st.set_page_config(page_title="Toggle con tecla", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Capturar tecla desde el componente React
key_pressed = my_key_listener(key="listener")

if key_pressed == "Enter":  # puedes cambiar la tecla
    st.session_state.toggle = not st.session_state.toggle
    st.rerun()

st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")
st.write("Última tecla detectada:", key_pressed)
