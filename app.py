# cronometro_shift.py
import streamlit as st
import time
from datetime import datetime, timedelta
from my_key_listener import my_key_listener

st.set_page_config(page_title="⏱️ Cronómetro con Shift", layout="centered")

# =======================
# ESTADO
# =======================
if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed" not in st.session_state:
    st.session_state.elapsed = timedelta(0)

# =======================
# TOGGLE
# =======================
def toggle():
    if not st.session_state.running:
        st.session_state.start_time = datetime.now()
        st.session_state.running = True
    else:
        st.session_state.running = False
        st.session_state.start_time = None
        st.session_state.elapsed = timedelta(0)

# =======================
# KEY LISTENER
# =======================
key = my_key_listener(key="listener")
if key == "Shift":
    toggle()
    st.rerun()

# =======================
# UI
# =======================
st.title("⏱️ Cronómetro con botón único / tecla Shift")

label = "⛔ Detener" if st.session_state.running else "🟢 Iniciar"
if st.button(label):
    toggle()
    st.rerun()

placeholder = st.empty()

if st.session_state.running and st.session_state.start_time:
    # Actualizar cronómetro
    elapsed = datetime.now() - st.session_state.start_time
    st.session_state.elapsed = elapsed
    placeholder.markdown(f"### ⏱️ Duración: {str(elapsed).split('.')[0]}")
    time.sleep(1)
    st.rerun()
else:
    # Mostrar 00:00:00 cuando está detenido
    placeholder.markdown("### ⏱️ Duración: 00:00:00")

st.caption(f"Última tecla detectada: {key}")
