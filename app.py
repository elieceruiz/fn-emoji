# app.py
import streamlit as st
import time
import pytz
from datetime import datetime
from pymongo import MongoClient
from my_key_listener import my_key_listener

st.set_page_config(page_title="Teclonómetro", layout="centered")

# ==========================
# Conexión MongoDB
# ==========================
mongo_uri = st.secrets["mongo_uri"]
client = MongoClient(mongo_uri)
db = client["teclometro_db"]
collection = db["sesiones"]

tz = pytz.timezone("America/Bogota")

# ==========================
# Inicializar estados seguros
# ==========================
st.session_state.running = st.session_state.get("running", False)
st.session_state.start_time = st.session_state.get("start_time", 0.0)
st.session_state.start_timestamp = st.session_state.get("start_timestamp", None)
st.session_state.elapsed_time = st.session_state.get("elapsed_time", 0.0)
st.session_state.last_key = st.session_state.get("last_key", None)

# ==========================
# Funciones
# ==========================
def start_timer():
    if not st.session_state.running:
        st.session_state.start_time = time.time()
        st.session_state.start_timestamp = datetime.now(tz)
        st.session_state.running = True

def reset_timer():
    if st.session_state.start_timestamp:
        end_timestamp = datetime.now(tz)
        elapsed = st.session_state.elapsed_time + (time.time() - st.session_state.start_time)

        # Guardar una sesión completa
        doc = {
            "inicio": st.session_state.start_timestamp,
            "fin": end_timestamp,
            "duracion_seg": elapsed,
            "duracion_formateada": f"{int(elapsed//3600):02d}:{int((elapsed%3600)//60):02d}:{int(elapsed%60):02d}"
        }
        collection.insert_one(doc)

    # Reiniciar todo
    st.session_state.running = False
    st.session_state.elapsed_time = 0.0
    st.session_state.start_time = 0.0
    st.session_state.start_timestamp = None

# ==========================
# UI
# ==========================
st.markdown("# Teclonómetro")

st.info("""
**Instrucciones**  
- Presiona **Delete** para iniciar el cronómetro.  
- Presiona **Shift** para detener y guardar la sesión.  
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
    if st.button("Detener y guardar", use_container_width=True):
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
# Mostrar sesiones guardadas
# ==========================
st.subheader("Histórico de sesiones")
docs = list(collection.find().sort("inicio", -1).limit(10))
if docs:
    table = []
    for d in docs:
        table.append({
            "Inicio": d["inicio"].strftime("%Y-%m-%d %H:%M:%S"),
            "Fin": d["fin"].strftime("%Y-%m-%d %H:%M:%S"),
            "Duración": d["duracion_formateada"]
        })
    st.table(table)
else:
    st.write("Sin sesiones registradas.")

# ==========================
# Auto actualización
# ==========================
if st.session_state.running:
    time.sleep(0.1)
    st.rerun()