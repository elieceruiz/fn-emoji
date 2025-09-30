# cronometro_shift.py
import streamlit as st
from datetime import datetime, timedelta
from my_key_listener import my_key_listener

st.set_page_config("⏱️ Cronómetro Toggle", layout="centered")
st.title("⏱️ Cronómetro con botón único / tecla Shift")

# ===============================
# Estado base
# ===============================
if "inicio" not in st.session_state:
    st.session_state.inicio = None
if "corriendo" not in st.session_state:
    st.session_state.corriendo = False
if "ultima_tecla" not in st.session_state:
    st.session_state.ultima_tecla = None

# ===============================
# Funciones
# ===============================
def toggle():
    if not st.session_state.corriendo:
        st.session_state.inicio = datetime.now()
        st.session_state.corriendo = True
    else:
        st.session_state.corriendo = False
        st.session_state.inicio = None

# ===============================
# Listener de tecla
# ===============================
key = my_key_listener(key="listener")
if key:
    st.session_state.ultima_tecla = key

if key == "Shift":
    toggle()
    st.rerun()

# ===============================
# Botón único
# ===============================
label = "🟢 Iniciar / Shift" if not st.session_state.corriendo else "⏹️ Detener / Shift"
if st.button(label):
    toggle()
    st.rerun()

# ===============================
# Cronómetro con autorefresh
# ===============================
placeholder = st.empty()

if st.session_state.corriendo and st.session_state.inicio:
    # refrescar cada 1 segundo
    st_autorefresh = st.experimental_rerun  # compatibilidad
    st.experimental_set_query_params(refresh=str(datetime.now()))  # hack
    ahora = datetime.now()
    segundos = int((ahora - st.session_state.inicio).total_seconds())
    duracion = str(timedelta(seconds=segundos))
    placeholder.markdown(f"### ⏱️ Duración: {duracion}")
else:
    placeholder.markdown("### ⏱️ Duración: 00:00:00")
