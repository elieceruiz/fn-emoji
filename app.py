# cronometro_shift.py
import streamlit as st
import time
from datetime import datetime, timedelta
from my_key_listener import my_key_listener  # tu componente React ya hecho

# =======================
# CONFIG
# =======================
st.set_page_config(page_title="⏱️ Cronómetro con botón único / tecla Shift", layout="centered")

# =======================
# ESTADO INICIAL
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
        # Arranca cronómetro
        st.session_state.start_time = datetime.now()
        st.session_state.running = True
    else:
        # Detiene y resetea
        st.session_state.running = False
        st.session_state.elapsed = timedelta(0)
        st.session_state.start_time = None

# =======================
# LISTENER DE TECLA
# =======================
key = my_key_listener(key="listener")

# Si se presiona Shift → actúa como clic al botón
if key == "Shift":
    toggle_cronometro()
    st.rerun()

# =======================
# INTERFAZ
# =======================
st.title("⏱️ Cronómetro con botón único / tecla Shift")
st.write("Presiona el botón o la tecla Shift para alternar.")

# Botón único
btn_label = "⛔ Detener" if st.session_state.running else "🟢 Iniciar"
if st.button(btn_label):
    toggle_cronometro()
    st.rerun()

# =======================
# CRONÓMETRO EN VIVO
# =======================
placeholder = st.empty()

if st.session_state.running:
    # Mientras esté corriendo, actualiza duración
    elapsed = datetime.now() - st.session_state.start_time
    st.session_state.elapsed = elapsed
    placeholder.subheader("⏱️ Duración: " + str(elapsed).split(".")[0])
    # Forzar actualización
    time.sleep(1)
    st.rerun()
else:
    # Cuando no corre, mostrar el valor congelado (o 00:00:00 si se reseteó)
    placeholder.subheader("⏱️ Duración: " + str(st.session_state.elapsed).split(".")[0])

st.write("Última tecla detectada:", key)
