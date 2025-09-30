# app.py
import streamlit as st
from datetime import datetime, timedelta
import pytz
from my_key_listener import my_key_listener

st.set_page_config(page_title="⏱ Cronómetro con Shift", layout="centered")
tz = pytz.timezone("America/Bogota")

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
        st.session_state.start_time = datetime.now(tz)

# ==========================
# DETECTOR TECLA (Shift)
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
# AUTOREFRESH
# ==========================
if st.session_state.running:
    st_autorefresh = getattr(st, "autorefresh", None)
    if st_autorefresh:
        st_autorefresh(interval=1000, key="tick")

# ==========================
# CRONÓMETRO
# ==========================
if st.session_state.running and st.session_state.start_time:
    elapsed = datetime.now(tz) - st.session_state.start_time
    tiempo = str(timedelta(seconds=int(elapsed.total_seconds())))
    st.title(f"⏱ {tiempo}")
else:
    st.title("⏱ 00:00:00")

# ==========================
# DEBUG
# ==========================
st.caption(f"Última tecla detectada: {key}")
