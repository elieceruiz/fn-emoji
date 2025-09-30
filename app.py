# app.py
import streamlit as st
from datetime import datetime, timedelta
import time
from my_key_listener import my_key_listener  # Componente React personalizado para detectar eventos de teclado

# Inicializamos variables en el estado de sesión de Streamlit
if "running" not in st.session_state:
    # Controla si el cronómetro está activo o detenido
    st.session_state.running = False
if "start_time" not in st.session_state:
    # Guarda la hora de inicio del cronómetro para calcular el tiempo transcurrido
    st.session_state.start_time = None

# Función para alternar el estado del cronómetro: inicia o detiene y reinicia el tiempo
def toggle_cronometro():
    if st.session_state.running:
        # Si está corriendo, detener y limpiar tiempo de inicio
        st.session_state.running = False
        st.session_state.start_time = None
    else:
        # Si está detenido, iniciar y fijar tiempo de inicio actual
        st.session_state.running = True
        st.session_state.start_time = datetime.now()

# Llamamos al componente React para detectar la última tecla presionada
key = my_key_listener(key="listener")

# Si se detecta que la tecla presionada es Shift, alternamos el cronómetro y reiniciamos la app
if key == "Shift":
    toggle_cronometro()
    st.rerun()  # Reinicia la ejecución del script para reflejar el cambio inmediatamente

st.title("⏱️ Cronómetro con tecla Shift")

# Si el cronómetro está activo y tiene un tiempo de inicio registrado, mostramos el tiempo transcurrido
if st.session_state.running and st.session_state.start_time:
    elapsed = datetime.now() - st.session_state.start_time  # Calculamos diferencia temporal
    # Mostramos el tiempo transcurrido sin la parte decimal de microsegundos
    st.markdown(f"### Tiempo transcurrido: {str(elapsed).split('.')[0]}")
    time.sleep(1)  # Pausamos un segundo para evitar sobrecarga y controlar actualización
    st.rerun()  # Volvemos a ejecutar el script para actualizar el tiempo mostrado
else:
    # Si no está corriendo, indicamos que el cronómetro está detenido
    st.markdown("### Cronómetro detenido")

# Botón visible como alternativa para iniciar o parar el cronómetro manualmente
if st.button("Iniciar/Parar"):
    toggle_cronometro()
    st.rerun()  # Reiniciamos ejecución para mostrar el estado actualizado
