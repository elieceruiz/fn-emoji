# app.py
import streamlit as st
import time
from my_key_listener import my_key_listener

st.set_page_config(page_title="Teclonómetro", layout="centered")

# Inicializar estados en session_state
if "running" not in st.session_state:
    st.session_state.running = False  # Cronómetro detenido inicialmente
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0  # Tiempo de inicio
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0.0  # Tiempo acumulado
if "last_key" not in st.session_state:
    st.session_state.last_key = None  # Última tecla detectada

# Función para iniciar el cronómetro
def start_timer():
    if not st.session_state.running:  # Solo iniciar si no está corriendo
        st.session_state.start_time = time.time()
        st.session_state.running = True

# Función para reiniciar y detener el cronómetro
def reset_timer():
    st.session_state.running = False
    st.session_state.elapsed_time = 0.0
    st.session_state.start_time = 0.0

# Título
st.markdown("# Teclonómetro")

# Instrucciones
st.info("""
**Instrucciones**  
- Presiona **Delete** para iniciar el cronómetro.  
- Presiona **Shift** para reiniciar y detener.  
- Usa los botones para control manual.
""")

# Detectar tecla
key = my_key_listener(key="listener")

# Lógica de teclas
if key != st.session_state.last_key:  # Evitar repeticiones rápidas
    st.session_state.last_key = key
    if key == "Delete":  # Delete inicia el cronómetro
        start_timer()
        st.rerun()
    elif key == "Shift":  # Shift reinicia y detiene
        reset_timer()
        st.rerun()

# Botones para control manual
col1, col2 = st.columns(2)
with col1:
    if st.button("Iniciar ˋ[Supr/Delete]ˋ", use_container_width=True):
        start_timer()
        st.rerun()
with col2:
    if st.button("Reiniciar ˋ[Shift]ˋ", use_container_width=True):
        reset_timer()
        st.rerun()

# Calcular tiempo transcurrido
if st.session_state.running:
    current_time = st.session_state.elapsed_time + (time.time() - st.session_state.start_time)
else:
    current_time = st.session_state.elapsed_time

# Formatear tiempo como HH:MM:SS
hours = int(current_time // 3600)
minutes = int((current_time % 3600) // 60)
seconds = int(current_time % 60)
formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Mostrar cronómetro
st.markdown(f"### {formatted_time}", unsafe_allow_html=True)

# Mostrar estado
if st.session_state.running:
    st.success("Estado: Corriendo")
else:
    st.error("Estado: Detenido")

# Mostrar última tecla detectada
st.write("Última tecla:", key if key else "Ninguna")

# Emoji para feedback visual
emoji = "🏃‍♂️" if st.session_state.running else "🛑"
st.markdown(f"## {emoji}", unsafe_allow_html=True)

# Actualización automática solo si está corriendo
if st.session_state.running:
    time.sleep(0.1)  # Pausa para evitar reruns demasiado rápidos
    st.rerun()
