# app.py
import streamlit as st
import time
from pymongo import MongoClient
from my_key_listener import my_key_listener
from datetime import datetime, timezone
import pytz

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="Teclonómetro", layout="centered")

# Leer Mongo desde secrets
mongo_uri = st.secrets["mongo_uri"]
client = MongoClient(mongo_uri)
db = client["teclonometro"]           # Base de datos
collection = db["cronometro"]         # Colección estado cronómetro
logs = db["cronometro_logs"]          # Colección para historial

# ID único para tu cronómetro
CRONO_ID = "principal"

# Zona horaria de Colombia
bogota_tz = pytz.timezone("America/Bogota")

# ========================
# Helpers DB
# ========================
def get_state():
    state = collection.find_one({"_id": CRONO_ID})
    if not state:
        state = {
            "_id": CRONO_ID,
            "running": False,
            "start_time": None,
            "paused_time": 0.0
        }
        collection.insert_one(state)
    return state

def update_state(updates: dict):
    collection.update_one({"_id": CRONO_ID}, {"$set": updates}, upsert=True)

def log_event(action: str):
    """Guardar logs de inicio / reinicio con hora UTC"""
    logs.insert_one({
        "action": action,
        "timestamp_utc": datetime.now(timezone.utc)
    })

def get_logs():
    """Devuelve logs con hora convertida a Colombia"""
    cursor = logs.find().sort("timestamp_utc", -1)  # más recientes arriba
    data = []
    for doc in cursor:
        ts_local = doc["timestamp_utc"].astimezone(bogota_tz)
        data.append({
            "Acción": doc["action"],
            "Hora (Bogotá)": ts_local.strftime("%Y-%m-%d %H:%M:%S")
        })
    return data

# ========================
# Lógica cronómetro
# ========================
state = get_state()

def start_timer():
    if not state["running"]:
        if state["start_time"] is None:
            update_state({
                "start_time": time.time(),
                "paused_time": 0.0,
                "running": True
            })
        else:
            new_start = time.time() - state["paused_time"]
            update_state({
                "start_time": new_start,
                "running": True
            })
        log_event("Iniciar")

def reset_timer():
    update_state({
        "running": False,
        "start_time": None,
        "paused_time": 0.0
    })
    log_event("Reiniciar")

# ========================
# UI
# ========================
st.markdown("# Teclonómetro")
st.info("""
**Instrucciones**  
- Presiona **Delete** para iniciar el cronómetro.  
- Presiona **Shift** para reiniciar y detener.  
- Usa los botones para control manual.
""")

# Detectar tecla
key = my_key_listener(key="listener")

if key == "Delete":
    start_timer()
    st.rerun()
elif key == "Shift":
    reset_timer()
    st.rerun()

# Botones
col1, col2 = st.columns(2)
with col1:
    if st.button("Iniciar", use_container_width=True):
        start_timer()
        st.rerun()
with col2:
    if st.button("Reiniciar", use_container_width=True):
        reset_timer()
        st.rerun()

# ========================
# Calcular tiempo
# ========================
state = get_state()

if state["start_time"] is not None:
    if state["running"]:
        elapsed = time.time() - state["start_time"]
        update_state({"paused_time": elapsed})
    else:
        elapsed = state["paused_time"]
else:
    elapsed = 0.0

# Formato HH:MM:SS
hours = int(elapsed // 3600)
minutes = int((elapsed % 3600) // 60)
seconds = int(elapsed % 60)
formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Mostrar cronómetro
st.markdown(f"### {formatted}")
st.write("Última tecla:", key if key else "Ninguna")
emoji = "🏃‍♂️" if state["running"] else "🛑"
st.markdown(f"## {emoji}")

# ========================
# Mostrar logs en tabla
# ========================
st.subheader("Historial de acciones (hora Bogotá)")
data = get_logs()
if data:
    st.dataframe(data)
else:
    st.info("No hay registros aún.")

# Refrescar en bucle
if state["running"]:
    time.sleep(0.5)
    st.rerun()