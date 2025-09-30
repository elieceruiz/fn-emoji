# app.py
import streamlit as st
from datetime import datetime, timedelta
import time
from my_key_listener import my_key_listener

# Estado inicial
if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None

def toggle_cronometro():
    if st.session_state.running:
        st.session_state.running = False
        st.session_state.start_time = None  # Limpia el tiempo para reiniciar a cero
    else:
        st.session_state.running = True
        st.session_state.start_time = datetime.now()

key = my_key_listener(key="listener")

# Si presionas Shift, cambia estado y reinicia el contador
if key == "Shift":
    toggle_cronometro()
    st.rerun()

st.title("⏱️ Cronómetro con Shift")

if st.session_state.running and st.session_state.start_time:
    elapsed = datetime.now() - st.session_state.start_time
    st.markdown(f"### Tiempo transcurrido: {str(elapsed).split('.')[0]}")
    time.sleep(1)
    st.experimental_rerun()
else:
    st.markdown("### Cronómetro detenido")

# Botón manual para iniciar/parar y reiniciar
if st.button("Iniciar/Parar"):
    toggle_cronometro()
    st.rerun()
