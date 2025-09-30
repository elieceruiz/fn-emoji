# app.py
import streamlit as st
from datetime import datetime

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

st.title("🕰️ Cronómetro Fase 1")

if st.button("Iniciar/Parar"):
    toggle_cronometro()

if st.session_state.running:
    st.write(f"Cronómetro iniciado a las {st.session_state.start_time}")
else:
    st.write("Cronómetro detenido")
