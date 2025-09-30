# cronometro_shift.py
import streamlit as st
import time
from datetime import datetime, timedelta
from my_key_listener import my_key_listener  # el mismo usado antes

st.set_page_config("⏱️ Cronómetro Toggle", layout="centered")
st.title("⏱️ Cronómetro con botón único / tecla Shift")

# ===============================
# Estado base
# ===============================
if "inicio" not in st.session_state:
    st.session_state.inicio = None
if "corriendo" not in st.session_state:
    st.session_state.corriendo = False
if "ultima_tecla" not in st.session_state:
    st.session_state.ultima_tecla = None

# ===============================
# Funciones
# ===============================
def toggle():
    if not st.session_state.corriendo:
        # Iniciar
        st.session_state.inicio = datetime.now()
        st.session_state.corriendo = True
    else:
        # Detener y resetear
        st.session_state.corriendo = False
        st.session_state.inicio = None

# ===============================
# Listener de tecla
# ===============================
key = my_key_listener(key="listener")
if key:
    st.session_state.ultima_tecla = key

if key == "Shift":
    toggle()
    st.rerun()

# ===============================
# Botón único
# ===============================
label = "🟢 Iniciar / Shift" if not st.session_state.corriendo else "⏹️ Detener / Shift"
if st.button(label):
    toggle()
    st.rerun()

# ===============================
# Cronómetro
# ===============================
marcador = st.empty()

if st.session_state.corriendo and st.session_state.inicio:
    while st.session_state.corriendo:
        ahora = datetime.now()
        segundos = int((ahora - st.session_state.inicio).total_seconds())
        duracion = str(timedelta(seconds=segundos))
        marcador.markdown(f"### ⏱️ Duración: {duracion}")
        time.sleep(1)
else:
    marcador.markdown("### ⏱️ Duración: 00:00:00")

# Debug opcional
st.caption(f"Última tecla detectada: {st.session_state.ultima_tecla}")
