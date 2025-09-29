import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Toggle con tecla", layout="centered")

# Estado inicial
if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Ejecuta JS y devuelve la última tecla presionada
key_pressed = streamlit_js_eval(
    js_expressions="new Promise(resolve => {document.addEventListener('keydown', e => resolve(e.key));})",
    key="key_event"
)

# Si se detecta una tecla específica, cambia el estado
if key_pressed == "Delete":   # aquí puedes poner "Enter", "Shift", etc.
    st.session_state.toggle = not st.session_state.toggle
    st.rerun()

# Mostrar estado
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")

# Debug
st.write("Última tecla detectada:", key_pressed)