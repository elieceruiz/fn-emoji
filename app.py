# app.py
import streamlit as st
from datetime import datetime, timedelta
from my_key_listener import my_key_listener

st.set_page_config(page_title="⏱ Cronómetro con Enter", layout="centered")

# ==========================
# ESTADOS
# ==========================
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "running" not in st.session_state:
    st.session_state.running = False

# ==========================
# FUNCIONES
# ==========================
def start_timer():
    st.session_state.start_time = datetime.now()
    st.session_state.running = True

def stop_timer():
    st.session_state.running = False
    st.session_state.start_time = None

# ==========================
# DETECTOR TECLA (Enter)
# ==========================
key = my_key_listener(key="listener")

if key == "Enter":
    if st.session_state.running:
        stop_timer()
    else:
        start_timer()
    st.rerun()

# ==========================
# BOTÓN
# ==========================
if st.button("▶️ Arrancar / ⏹ Parar"):
    if st.session_state.running:
        stop_timer()
    else:
        start_timer()
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
    elapsed = datetime.now() - st.session_state.start_time
    tiempo = str(timedelta(seconds=int(elapsed.total_seconds())))
    st.title(f"⏱ {tiempo}")
else:
    st.title("⏱ 00:00:00")

# ==========================
# DEBUG
# ==========================
st.write("Última tecla detectada:", key)
