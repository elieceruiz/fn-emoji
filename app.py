# app.py
import streamlit as st
import time
from my_key_listener import my_key_listener

st.set_page_config(page_title="Teclonómetro", layout="centered")

# ==========================
# Inicializar estados seguros
# ==========================
st.session_state.running = st.session_state.get("running", False)
st.session_state.start_time = st.session_state.get("start_time", 0.0)
st.session_state.elapsed_time = st.session_state.get("elapsed_time", 0.0)
st.session_state.last_key = st.session_state.get("last_key", None)

# ==========================
# Funciones de control
# ==========================
def start_timer():
    if not st.session_state.running:
        st.session_state.start_time = time.time()
        st.session_state.running = True

def reset_timer():
    st.session_state.running = False
    st.session_state.elapsed_time = 0.0
    st.session_state.start_time = 0.0

# ==========================
# UI
# ==========================
st.markdown("# Teclonómetro")

st.info("""
**Instrucciones**  
- Presiona **Delete** para iniciar el cronómetro.  
- Presiona **Shift** para reiniciar y detener.  
- Usa los botones para control manual.
""")

# Detectar tecla
key = my_key_listener(key="listener")

# Lógica de teclas
if key != st.session_state.last_key:  
    st.session_state.last_key = key
    if key == "Delete":
        start_timer()
        st.rerun()
    elif key == "Shift":
        reset_timer()
        st.rerun()

# Botones manuales
col1, col2 = st.columns(2)
with col1:
    if st.button("Iniciar", use_container_width=True):
        start_timer()
        st.rerun()
with col2:
    if st.button("Reiniciar", use_container_width=True):
        reset_timer()
        st.rerun()

# ==========================
# Cronómetro
# ==========================
if st.session_state.running:
    current_time = st.session_state.elapsed_time + (time.time() - st.session_state.start_time)
else:
    current_time = st.session_state.elapsed_time

hours = int(current_time // 3600)
minutes = int((current_time % 3600) // 60)
seconds = int(current_time % 60)
formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

st.markdown(f"### {formatted_time}", unsafe_allow_html=True)

# Estado
if st.session_state.running:
    st.success("Estado: Corriendo")
else:
    st.error("Estado: Detenido")

# Última tecla
st.write("Última tecla:", key if key else "Ninguna")

# Emoji
emoji = "🏃‍♂️" if st.session_state.running else "🛑"
st.markdown(f"## {emoji}", unsafe_allow_html=True)

# ==========================
# Auto actualización
# ==========================
if st.session_state.running:
    time.sleep(0.1)
    st.rerun()