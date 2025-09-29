import streamlit as st
from streamlit_key_events import key_events   # <-- con guion bajo

st.set_page_config(page_title="Toggle con tecla", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Captura eventos de teclado
events = key_events()

if events.key == "Delete":  # cambia la tecla a gusto: "Enter", "Shift", etc.
    st.session_state.toggle = not st.session_state.toggle
    st.rerun()

# Mostrar estado
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")

st.write("Última tecla detectada:", events)