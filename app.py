# app.py
import streamlit as st
from my_key_listener import my_key_listener

st.set_page_config(page_title="Toggle con tecla", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = True  # estado inicial = feliz

key = my_key_listener(key="listener")

# Solo con Shift se alterna el toggle, simula un botón clickeado
if key == "Shift":
    st.session_state.toggle = not st.session_state.toggle

emoji = "😊" if st.session_state.toggle else "😢"

st.markdown(f"### {emoji}")
st.write("Última tecla detectada:", key)
