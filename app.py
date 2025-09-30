# app.py
import streamlit as st
import time
from datetime import datetime
from my_key_listener import my_key_listener

st.set_page_config(page_title="⏱ Cronómetro con tecla", layout="centered")

# ==========================
# ESTADOS INICIALES
# ==========================
if "start_time" not in st.session_state:
    st.session_state.start_time = None

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

def toggle_timer():
    if st.session_state.running:
        reset_timer()
    else:
        start_timer()

# ==========================
# CAPTURA DE TECLA
# ==========================
key = my_key_listener(key="listener")

if key == "Delete":  # tecla Suprimir
    toggle_timer()
    key = None  # consumir evento

# ==========================
# BOTÓN DE CONTROL
# ==========================
st.button("▶️ Arrancar / 🔄 Reiniciar", on_click=toggle_timer)

# ==========================
# VISUALIZACIÓN
# ==========================
st.title("⏱ Cronómetro")
placeholder = st.empty()

while st.session_state.running:
    elapsed = datetime.now() - st.session_state.start_time
    h, r = divmod(elapsed.seconds, 3600)
    m, s = divmod(r, 60)
    placeholder.markdown(f"### {h:02d}:{m:02d}:{s:02d}")
    time.sleep(1)
    st.rerun()

if not st.session_state.running:
    placeholder.markdown("### 00:00:00")
