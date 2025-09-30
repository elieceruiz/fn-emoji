import streamlit as st
import time
from my_key_listener import my_key_listener

st.set_page_config(page_title="Cronómetro con tecla", layout="centered")

# Inicializar estados en session_state
if "running" not in st.session_state:
    st.session_state.running = False  # Cronómetro detenido inicialmente
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0  # Tiempo de inicio
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0.0  # Tiempo acumulado
if "last_key" not in st.session_state:
    st.session_state.last_key = None  # Última tecla detectada

# Función para alternar el estado del cronómetro
def toggle_timer():
    if st.session_state.running:
        # Detener el cronómetro y acumular el tiempo
        st.session_state.elapsed_time += time.time() - st.session_state.start_time
        st.session_state.running = False
    else:
        # Iniciar el cronómetro
        st.session_state.start_time = time.time()
        st.session_state.running = True

# Función para reiniciar el cronómetro
def reset_timer():
    st.session_state.running = False
    st.session_state.elapsed_time = 0.0
    st.session_state.start_time = 0.0

# Detectar tecla
key = my_key_listener(key="listener")

# Alternar cronómetro si se presiona Delete o Shift (evitar repeticiones rápidas)
if key in ["Delete", "Shift"] and key != st.session_state.last_key:
    st.session_state.last_key = key
    toggle_timer()
    st.rerun()  # Forzar actualización para reflejar el cambio de estado

# Botones para control manual
col1, col2 = st.columns(2)
with col1:
    if st.button("Iniciar/Detener"):
        toggle_timer()
        st.rerun()
with col2:
    if st.button("Reiniciar"):
        reset_timer()
        st.rerun()

# Calcular tiempo transcurrido
if st.session_state.running:
    current_time = st.session_state.elapsed_time + (time.time() - st.session_state.start_time)
else:
    current_time = st.session_state.elapsed_time

# Formatear tiempo como MM:SS
minutes = int(current_time // 60)
seconds = int(current_time % 60)
formatted_time = f"{minutes:02d}:{seconds:02d}"

# Mostrar cronómetro
st.markdown(f"### Cronómetro: {formatted_time}")
st.write("Estado:", "Corriendo" if st.session_state.running else "Detenido")
st.write("Última tecla detectada:", key)

# Emoji para feedback visual
emoji = "🏃‍♂️" if st.session_state.running else "🛑"
st.markdown(f"#### {emoji}")

# Actualización automática solo si está corriendo
if st.session_state.running:
    time.sleep(0.1)  # Pequeña pausa para evitar reruns demasiado rápidos
    st.rerun()