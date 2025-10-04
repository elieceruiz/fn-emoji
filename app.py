# app.py
import streamlit as st
import time
from datetime import datetime
from pymongo import MongoClient
import pytz
from my_key_listener import my_key_listener

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Teclonómetro", layout="centered")
st.markdown("# ⌨️")

# Zona horaria de Colombia
tz = pytz.timezone("America/Bogota")

# Conectar a MongoDB desde secrets
mongo_uri = st.secrets["mongo_uri"]
client = MongoClient(mongo_uri)
db = client["teclonometro_db"]
collection = db["sesiones"]

# ==============================
# ESTADOS
# ==============================
if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0.0
if "last_key" not in st.session_state:
    st.session_state.last_key = None
if "inicio_dt" not in st.session_state:
    st.session_state.inicio_dt = None

# ==============================
# FUNCIONES
# ==============================
def start_timer():
    st.session_state.start_time = time.time()
    st.session_state.running = True
    st.session_state.inicio_dt = datetime.now(tz)

def stop_and_save():
    # ✅ Validación: no hacer nada si no hay inicio registrado
    if st.session_state.inicio_dt is None:
        return

    fin_dt = datetime.now(tz)
    duracion = st.session_state.elapsed_time + (time.time() - st.session_state.start_time)

    # Formatear duración a HH:MM:SS
    h = int(duracion // 3600)
    m = int((duracion % 3600) // 60)
    s = int(duracion % 60)
    duracion_str = f"{h:02d}:{m:02d}:{s:02d}"

    # Guardar en Mongo
    collection.insert_one({
        "inicio": st.session_state.inicio_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "fin": fin_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "duracion": duracion_str
    })

    # Reiniciar estados
    st.session_state.running = False
    st.session_state.elapsed_time = 0.0
    st.session_state.start_time = 0.0
    st.session_state.inicio_dt = None

# ==============================
# INSTRUCCIONES
# ==============================
st.info("""
**Instrucciones**  
- Presiona **`Delete`** para iniciar el cronómetro.  
- Presiona **`Shift`** para detener y guardar la sesión.  
- También puedes usar el botón central para control manual.
""")

# ==============================
# DETECCIÓN DE TECLAS
# ==============================
key = my_key_listener(key="listener")

if key != st.session_state.last_key:
    st.session_state.last_key = key
    if key == "Delete":
        start_timer()
        st.rerun()
    elif key == "Shift":
        stop_and_save()
        st.rerun()

# ==============================
# CRONÓMETRO
# ==============================
if st.session_state.running:
    current_time = st.session_state.elapsed_time + (time.time() - st.session_state.start_time)
else:
    current_time = st.session_state.elapsed_time

h = int(current_time // 3600)
m = int((current_time % 3600) // 60)
s = int(current_time % 60)
formatted_time = f"{h:02d}:{m:02d}:{s:02d}"

st.markdown(f"## {formatted_time}")

# Estado visual
if st.session_state.running:
    st.success("Estado: Corriendo")
else:
    st.error("Estado: Detenido")

st.write("Última tecla:", f"`{key}`" if key else "Ninguna")

# ==============================
# BOTÓN ÚNICO MINIMALISTA
# ==============================
if st.session_state.running:
    label = "🔴 `Shift`"
else:
    label = "🟢 `Delete`"

if st.button(label, use_container_width=True):
    if not st.session_state.running:
        start_timer()
    else:
        stop_and_save()
    st.rerun()

# ==============================
# ACTUALIZACIÓN AUTOMÁTICA
# ==============================
if st.session_state.running:
    time.sleep(0.1)
    st.rerun()

# ==============================
# HISTÓRICO DE SESIONES
# ==============================
st.subheader("Histórico de sesiones")

sessions = list(collection.find().sort("_id", -1))

if sessions:
    formatted_data = []
    total = len(sessions)
    for idx, s in enumerate(sessions, start=1):
        inicio = s.get("inicio")
        fin = s.get("fin")
        duracion = s.get("duracion")

        # Ejemplo: "4 Oct 25 — 15:53:52"
        inicio_fmt = datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S").strftime("%-d %b %y — %H:%M:%S")
        fin_fmt = datetime.strptime(fin, "%Y-%m-%d %H:%M:%S").strftime("%-d %b %y — %H:%M:%S")

        # Duración: "0h 8m 2s"
        h, m, s = duracion.split(":")
        duracion_fmt = f"{int(h)}h {int(m)}m {int(s)}s"

        formatted_data.append({
            # 👇 ahora el más reciente recibe el número mayor
            "N°": total - idx + 1,
            "Inicio": inicio_fmt,
            "Fin": fin_fmt,
            "Duración": duracion_fmt
        })

    st.dataframe(formatted_data, use_container_width=True)
else:
    st.info("Aún no hay registros guardados.")