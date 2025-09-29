import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Test JS Eval", layout="centered")

st.write("👉 Presiona cualquier tecla en tu teclado")

# Esto debería capturar la primera tecla que presiones
key_pressed = streamlit_js_eval(
    js_expressions="new Promise(resolve => {document.addEventListener('keydown', e => resolve(e.key));})",
    key="test_key"
)

st.write("Última tecla detectada:", key_pressed)