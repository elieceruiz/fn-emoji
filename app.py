import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="⏱ Cronómetro Demo", layout="centered")

# ==========================
# ESTADOS
# ==========================
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "running" not in st.session_state:
    st.session_state.running = False
if "last_display" not in st.session_state:
    st.session_state.last_display = "00:00:00"

# ==========================
# FUNCIÓN
# ==========================
def toggle_timer():
    if st.session_state.running:
        # parar y reiniciar
        st.session_state.running = False
        st.session_state.start_time = None
        st.session_state.last_display = "00:00:00"
    else:
        # arrancar
        st.session_state.running = True
        st.session_state.start_time = datetime.now()

# ==========================
# BOTÓN
# ==========================
st.button("▶️ Arrancar / 🔄 Reiniciar", on_click=toggle_timer)

# ==========================
# CRONÓMETRO
# ==========================
if st.session_state.running and st.session_state.start_time:
    elapsed = datetime.now() - st.session_state.start_time
    h, r = divmod(elapsed.seconds, 3600)
    m, s = divmod(r, 60)
    st.session_state.last_display = f"{h:02d}:{m:02d}:{s:02d}"
    time.sleep(1)
    st.rerun()

st.title(f"⏱ {st.session_state.last_display}")
