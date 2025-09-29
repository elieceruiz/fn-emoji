# app.py
import streamlit as st
from my_key_listener import my_key_listener

st.set_page_config(page_title="Toggle con tecla", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False

key = my_key_listener(key="listener")
if key == "Enter":
    st.session_state.toggle = not st.session_state.toggle
    st.rerun()  # uso recomendado vs st.rerun()

st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")
st.write("Última tecla detectada:", key)
