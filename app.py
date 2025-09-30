# cronometro_shift.py
import streamlit as st
import time
from datetime import datetime, timedelta
from my_key_listener import my_key_listener  # tu componente React

# =======================
# CONFIG
# =======================
st.set_page_config(page_title="⏱️ Cronómetro con botón único / tecla Shift", layout="centered")

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
# FUNCIONES
# =======================
def toggle_cronometro():
    if not st.session_state.running:
        # Arranca
        st.session_state.start_time = datetime.now()
        st.session_state.running = True
    else:
        # Detiene y resetea
        st.session_state.running = False
        st.session_state.elapsed = timedelta(0)
        st.session_state.start_time = None

# =======================
# LISTENER TECLA
# =======================
key = my_key_listener(key="listener")
if key == "Shift":
    toggle_cronometro()
    st.rerun()

# =======================
# INTERFAZ
# =======================
st.title("⏱️ Cronómetro con botón único / tecla Shift")

btn_label = "⛔ Detener" if st.session_state.running else "🟢 Iniciar"
if st.button(btn_label):
    toggle_cronometro()
    st.rerun()

# =======================
# CRONÓMETRO
# =======================
placeholder = st.empty()

if st.session_state.running and st.session_state.start_time:
    # Mientras corre
    elapsed = datetime.now() - st.session_state.start_time
    st.session_state.elapsed = elapsed
    placeholder.subheader("⏱️ Duración: " + str(elapsed).split(".")[0])
    time.sleep(1)
    st.rerun()
else:
    # Cuando se detiene → muestra 00:00:00
    placeholder.subheader("⏱️ Duración: 00:00:00")

st.caption(f"Última tecla detectada: {key}")
