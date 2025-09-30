# app.py
import streamlit as st
from datetime import datetime, timedelta
import time
from my_key_listener import my_key_listener

if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None

def toggle_cronometro():
    st.write("DEBUG: toggle_cronometro called")
    if st.session_state.running:
        st.session_state.running = False
        st.session_state.end_time = datetime.now()
        st.write("DEBUG: Cronómetro detenido")
    else:
        st.session_state.running = True
        st.session_state.start_time = datetime.now()
        st.session_state.end_time = None
        st.write("DEBUG: Cronómetro iniciado")

key = my_key_listener(key="listener")
st.write(f"DEBUG: Última tecla detectada: {key}")

if key == "Shift":
    toggle_cronometro()
    st.rerun()

st.title("⏱️ Cronómetro activado con Shift")

if st.session_state.running:
    elapsed = datetime.now() - st.session_state.start_time
    st.markdown(f"### Duración: {str(elapsed).split('.')[0]}")
    time.sleep(1)  # esperar un segundo
    st.rerun()  # recargar para actualizar tiempo real
else:
    if "end_time" in st.session_state and st.session_state.end_time:
        elapsed = st.session_state.end_time - st.session_state.start_time
    else:
        elapsed = timedelta(seconds=0)
    st.markdown(f"### Duración: {str(elapsed).split('.')[0]}")

# Botón para toggle manual
if st.button("Iniciar/Parar"):
    toggle_cronometro()
    st.rerun()
