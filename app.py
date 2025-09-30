# app.py
import streamlit as st
import time
from datetime import datetime, timedelta
from my_key_listener import my_key_listener

st.set_page_config(page_title="⏱ Cronómetro con tecla", layout="centered")

# ==========================
# ESTADOS INICIALES
# ==========================
if "start_time" not in st.session_state:
    st.session_state.start_time = None  # no ha arrancado aún

if "running" not in st.session_state:
    st.session_state.running = False

# ==========================
# LÓGICA DEL CRONÓMETRO
# ==========================
def start_timer():
    st.session_state.start_time = datetime.now()
    st.session_state.running = True

def reset_timer():
    st.session_state.start_time = None
    st.session_state.running = False

# ==========================
# CAPTURA DE TECLA
# ==========================
key = my_key_listener(key="listener")

# Si presiono Suprimir → arranca o resetea
if key == "Delete":  # o "Shift"
    if not st.session_state.running:
        start_timer()
    else:
        reset_timer()
    key = None  # consumir evento

# ==========================
# VISUALIZACIÓN
# ==========================
st.title("⏱ Cronómetro")

placeholder = st.empty()

while st.session_state.running:
    elapsed = datetime.now() - st.session_state.start_time
    # Mostrar en formato H:M:S
    h, r = divmod(elapsed.seconds, 3600)
    m, s = divmod(r, 60)
    placeholder.markdown(f"### {h:02d}:{m:02d}:{s:02d}")
    time.sleep(1)
    st.rerun()

if not st.session_state.running:
    placeholder.markdown("### 00:00:00")
