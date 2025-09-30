# app.py
import streamlit as st
from datetime import datetime, timedelta
import time
from my_key_listener import my_key_listener  # componente React para detectar tecla Shift

# Estado inicial
if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None

def toggle_cronometro():
    if st.session_state.running:
        st.session_state.running = False
        st.session_state.end_time = datetime.now()
    else:
        st.session_state.running = True
        st.session_state.start_time = datetime.now()
        st.session_state.end_time = None

# Detectar tecla con el componente React
key = my_key_listener(key="listener")

# Si presionan Shift, toggle del cronómetro (simula clic)
if key == "Shift":
    toggle_cronometro()
    st.rerun()

st.title("⏱️ Cronómetro activado con Shift")

# Mostrar duración
if st.session_state.running:
    elapsed = datetime.now() - st.session_state.start_time
else:
    if "end_time" in st.session_state and st.session_state.end_time:
        elapsed = st.session_state.end_time - st.session_state.start_time
    else:
        elapsed = timedelta(seconds=0)

st.markdown(f"### Duración: {str(elapsed).split('.')[0]}")

# Botón toggle visible (opcional)
if st.button("Iniciar/Parar"):
    toggle_cronometro()
    st.rerun()
