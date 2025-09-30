# app.py
import streamlit as st
from datetime import datetime, timedelta
import time
from my_key_listener import my_key_listener  # Componente React que detecta teclas

# Inicializamos el estado para controlar el cronómetro
if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None

def toggle_cronometro():
    if st.session_state.running:
        st.session_state.running = False
        st.session_state.start_time = None
    else:
        st.session_state.running = True
        st.session_state.start_time = datetime.now()

# Detectamos la tecla con el componente React
key = my_key_listener(key="listener")

# Mostrar para diagnóstico qué tecla se detecta
st.write(f"Última tecla detectada: {key}")

# Si la tecla es Shift, toggle del cronómetro y rerun
if key == "Shift":
    toggle_cronometro()
    st.rerun()

st.title("⏱️ Cronómetro con tecla Shift")

if st.session_state.running and st.session_state.start_time:
    elapsed = datetime.now() - st.session_state.start_time
    st.markdown(f"### Tiempo transcurrido: {str(elapsed).split('.')[0]}")
    time.sleep(1)  # Pausa para refrescar cada segundo
    st.rerun()
else:
    st.markdown("### Cronómetro detenido")

# Botón manual para iniciar o parar
if st.button("Iniciar/Parar"):
    toggle_cronometro()
    st.rerun()
