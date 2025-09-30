# cronometro_front.py
import streamlit as st
import time
from datetime import datetime, timedelta

st.set_page_config("⏱️ Cronómetro Demo", layout="centered")
st.title("⏱️ Demo de Cronómetro en Front")

# Guardar estado del cronómetro
if "inicio" not in st.session_state:
    st.session_state.inicio = None
if "corriendo" not in st.session_state:
    st.session_state.corriendo = False

# Botón iniciar
if not st.session_state.corriendo:
    if st.button("🟢 Iniciar"):
        st.session_state.inicio = datetime.now()
        st.session_state.corriendo = True
        st.rerun()

# Botón detener
if st.session_state.corriendo:
    stop = st.button("⏹️ Detener")
    marcador = st.empty()

    while st.session_state.corriendo:
        ahora = datetime.now()
        segundos = int((ahora - st.session_state.inicio).total_seconds())
        duracion = str(timedelta(seconds=segundos))
        marcador.markdown(f"### ⏱️ Duración: {duracion}")

        if stop:
            st.session_state.corriendo = False
            st.success("✅ Cronómetro detenido.")
            break

        time.sleep(1)
