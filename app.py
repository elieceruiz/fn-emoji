import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Toggle con tecla", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False

key_pressed = streamlit_js_eval(
    js_expressions="new Promise(resolve => {document.addEventListener('keydown', e => resolve(e.key));})",
    key="key_event"
)

if key_pressed == "Delete":
    st.session_state.toggle = not st.session_state.toggle
    st.rerun()

st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")
st.write("Última tecla detectada:", key_pressed)