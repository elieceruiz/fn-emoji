import streamlit as st
import time
from datetime import datetime, timedelta
from my_key_listener import my_key_listener  # el mismo que usaste con emojis

st.set_page_config(page_title="⏱ Cronómetro con Shift", layout="centered")

# ==========================
# ESTADOS
# ==========================
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "running" not in st.session_state:
    st.session_state.running = False

# ==========================
# FUNCIÓN
# ==========================
def toggle_timer():
    if st.session_state.running:
        # parar y reiniciar
        st.session_state.running = False
        st.session_state.start_time = None
    else:
        # arrancar
        st.session_state.running = True
        st.session_state.start_time = datetime.now()

# ==========================
# TECLA SHIFT
# ==========================
key = my_key_listener(key="listener")

if key == "Shift":
    toggle_timer()
    st.rerun()

# ==========================
# BOTÓN
# ==========================
if st.button("▶️ Arrancar / 🔄 Reiniciar"):
    toggle_timer()
    st.rerun()

# ==========================
# CRONÓMETRO
# ==========================
placeholder = st.empty()

if st.session_state.running and st.session_state.start_time:
    while st.session_state.running:
        elapsed = datetime.now() - st.session_state.start_time
        tiempo = str(timedelta(seconds=int(elapsed.total_seconds())))
        placeholder.title(f"⏱ {tiempo}")

        time.sleep(1)  # espera 1 segundo antes de actualizar

        if not st.session_state.running:
            break
else:
    placeholder.title("⏱ 00:00:00")

st.write("Última tecla detectada:", key)
