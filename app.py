import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="⏱ Cronómetro con tecla", layout="centered")

# --- Inicialización ---
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

if "last_key" not in st.session_state:
    st.session_state.last_key = None

# --- Captura tecla con text_input ---
key = st.text_input("Escribe aquí y presiona ENTER (ej: shift)").lower()

if key == "shift":
    st.session_state.start_time = datetime.now()
    st.session_state.last_key = key
    st.experimental_rerun()

# --- Mostrar cronómetro ---
placeholder = st.empty()

while True:
    elapsed = datetime.now() - st.session_state.start_time
    segundos = int(elapsed.total_seconds())
    h = segundos // 3600
    m = (segundos % 3600) // 60
    s = segundos % 60
    placeholder.markdown(f"### ⏱ {h:02d}:{m:02d}:{s:02d}")
    time.sleep(1)
