# app.py
import streamlit as st
from datetime import datetime
from my_key_listener import my_key_listener

st.set_page_config(page_title="Cronómetro básico", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False  # cronómetro apagado inicialmente
if "start_time" not in st.session_state:
    st.session_state.start_time = None

def on_toggle():
    if st.session_state.toggle:
        st.session_state.toggle = False
        st.session_state.start_time = None
    else:
        st.session_state.toggle = True
        st.session_state.start_time = datetime.now()

key = my_key_listener(key="listener")

if key == "Shift":
    on_toggle()

button_clicked = st.button("Iniciar/Parar", on_click=on_toggle)

if st.session_state.toggle and st.session_state.start_time:
    elapsed = datetime.now() - st.session_state.start_time
    st.markdown(f"Tiempo transcurrido: {str(elapsed).split('.')[0]}")
else:
    st.markdown("Cronómetro detenido")

st.write("Última tecla detectada:", key)
