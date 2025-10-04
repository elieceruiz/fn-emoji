import streamlit as st
import time
from pymongo import MongoClient
from my_key_listener import my_key_listener

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Teclonómetro", layout="centered")

# Mongo
mongo_uri = st.secrets["mongo_uri"]
client = MongoClient(mongo_uri)
db = client["teclonometro"]
collection = db["cronometro"]

CRONO_ID = "principal"

# ==============================
# Helpers Mongo
# ==============================
def get_state():
    state = collection.find_one({"_id": CRONO_ID})
    if not state:
        state = {
            "_id": CRONO_ID,
            "running": False,
            "start_time": 0.0,
            "elapsed_time": 0.0,
            "last_key": None
        }
        collection.insert_one(state)
    return state

def update_state(updates: dict):
    collection.update_one({"_id": CRONO_ID}, {"$set": updates}, upsert=True)

# ==============================
# Inicializar estados
# ==============================
state = get_state()

if "running" not in st.session_state:
    st.session_state.running = state["running"]
if "start_time" not in st.session_state:
    st.session_state.start_time = state["start_time"]
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = state["elapsed_time"]
if "last_key" not in st.session_state:
    st.session_state.last_key = state["last_key"]

# ==============================
# Funciones cronómetro
# ==============================
def start_timer():
    if not st.session_state.running:
        st.session_state.start_time = time.time()
        st.session_state.running = True
        update_state({
            "running": True,
            "start_time": st.session_state.start_time,
            "elapsed_time": st.session_state.elapsed_time
        })

def reset_timer():
    st.session_state.running = False
    st.session_state.elapsed_time = 0.0
    st.session_state.start_time = 0.0
    update_state({
        "running": False,
        "start_time": 0.0,
        "elapsed_time": 0.0
    })

# ==============================
# UI
# ==============================
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
    update_state({"last_key": key})  # guardar tecla
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

# ==============================
# Calcular tiempo
# ==============================
if st.session_state.running:
    current_time = st.session_state.elapsed_time + (time.time() - st.session_state.start_time)
else:
    current_time = st.session_state.elapsed_time

# Guardar avance en Mongo
update_state({
    "running": st.session_state.running,
    "start_time": st.session_state.start_time,
    "elapsed_time": current_time,
    "last_key": st.session_state.last_key
})

# ==============================
# Mostrar cronómetro
# ==============================
hours = int(current_time // 3600)
minutes = int((current_time % 3600) // 60)
seconds = int(current_time % 60)
formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

st.markdown(f"### {formatted_time}")

if st.session_state.running:
    st.success("Estado: Corriendo")
else:
    st.error("Estado: Detenido")

st.write("Última tecla:", key if key else "Ninguna")

emoji = "🏃‍♂️" if st.session_state.running else "🛑"
st.markdown(f"## {emoji}")

# ==============================
# Auto-refresh
# ==============================
if st.session_state.running:
    time.sleep(0.1)
    st.rerun()