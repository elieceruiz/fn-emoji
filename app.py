# cronometro_front.py
import streamlit as st
import time
from datetime import datetime, timedelta
from my_key_listener import my_key_listener  # el mismo que ya usás en app.py

st.set_page_config("⏱️ Cronómetro Demo", layout="centered")
st.title("⏱️ Demo de Cronómetro en Front con tecla Shift")

# ===============================
# Estado base
# ===============================
if "inicio" not in st.session_state:
    st.session_state.inicio = None
if "corriendo" not in st.session_state:
    st.session_state.corriendo = False

# ===============================
# Funciones
# ===============================
def start():
    st.session_state.inicio = datetime.now()
    st.session_state.corriendo = True
    st.rerun()

def stop():
    st.session_state.corriendo = False
    st.success("✅ Cronómetro detenido.")
    st.rerun()

# ===============================
# Key listener (Shift)
# ===============================
key = my_key_listener(key="listener")

if key == "Shift":
    if not st.session_state.corriendo:
        start()
    else:
        stop()

# ===============================
# Interfaz
# ===============================
if not st.session_state.corriendo:
    if st.button("🟢 Iniciar"):
        start()
else:
    stop_button = st.button("⏹️ Detener")
    marcador = st.empty()

    while st.session_state.corriendo:
        ahora = datetime.now()
        segundos = int((ahora - st.session_state.inicio).total_seconds())
        duracion = str(timedelta(seconds=segundos))
        marcador.markdown(f"### ⏱️ Duración: {duracion}")

        if stop_button:
            stop()
            break

        time.sleep(1)

# Mostrar última tecla detectada (para debug)
st.caption(f"Última tecla detectada: {key}")
