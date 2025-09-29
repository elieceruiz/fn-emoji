import streamlit as st
from my_key_listener import my_key_listener

st.set_page_config(page_title="Emoji Toggle", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False

key = my_key_listener()

if key == "Delete":
    st.session_state.toggle = not st.session_state.toggle
    st.rerun()

st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")
st.write("Última tecla detectada:", key)
