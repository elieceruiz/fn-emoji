# app.py
import streamlit as st
from datetime import datetime, timedelta
import time
import pytz
from my_key_listener import my_key_listener

st.set_page_config(page_title="🌧️ Lluvia & Dev Tracker", layout="centered")

tz = pytz.timezone("America/Bogota")

# ===============================
# ESTADOS
# ===============================
if "eventos" not in st.session_state:
    st.session_state.eventos = {"dev_app": None, "mojada_lluvia": None}

if "historial" not in st.session_state:
    st.session_state.historial = {"dev_app": [], "mojada_lluvia": []}

# ===============================
# FUNCIONES
# ===============================
def toggle_event(tipo, label_fin):
    evento = st.session_state.eventos[tipo]
    if evento:  # finalizar
        fin = datetime.now(tz)
        st.session_state.historial[tipo].insert(
            0, (evento["inicio"], fin)
        )
        st.session_state.eventos[tipo] = None
        st.success(label_fin)
    else:  # iniciar
        st.session_state.eventos[tipo] = {"inicio": datetime.now(tz)}

def cronometro(tipo, label_inicio, label_fin):
    evento = st.session_state.eventos[tipo]
    if evento:
        hora_inicio = evento["inicio"]
        segundos = int((datetime.now(tz) - hora_inicio).total_seconds())
        st.success(f"{label_inicio} {hora_inicio.strftime('%H:%M:%S')}")
        cronometro = st.empty()
        stop_button = st.button("⏹️ Finalizar", key=f"stop_{tipo}")
        if stop_button:
            toggle_event(tipo, label_fin)
            st.rerun()
        for i in range(segundos, segundos + 100000):
            duracion = str(timedelta(seconds=i))
            cronometro.markdown(f"### ⏱️ Duración: {duracion}")
            time.sleep(1)
    else:
        if st.button("🟢 Iniciar", key=f"start_{tipo}"):
            toggle_event(tipo, label_fin=None)
            st.rerun()

def mostrar_historial(tipo, titulo):
    with st.expander(titulo):
        registros = st.session_state.historial[tipo]
        if not registros:
            st.info("📭 No hay registros todavía.")
        for i, (inicio, fin) in enumerate(registros, start=1):
            inicio_str = inicio.strftime("%Y-%m-%d %H:%M:%S")
            fin_str = fin.strftime("%Y-%m-%d %H:%M:%S") if fin else "⏳ En curso"
            duracion = str(fin - inicio) if fin else ""
            st.write(f"{i}. 🕒 **Inicio:** {inicio_str} | **Fin:** {fin_str} | **Duración:** {duracion}")

# ===============================
# DETECTOR TECLA
# ===============================
key = my_key_listener(key="listener")

if key == "Shift":
    # Cambia el estado SOLO para desarrollo (podés duplicar para lluvia también)
    toggle_event("dev_app", "✅ Registro de desarrollo finalizado.")
    st.rerun()

# ===============================
# INTERFAZ CON TABS
# ===============================
tab1, tab2 = st.tabs(["💻 Desarrollo", "🌧️ Mojadas"])

with tab1:
    st.subheader("⏳ Tiempo invertido en el desarrollo de la App")
    cronometro("dev_app",
               label_inicio="🟢 Desarrollo en curso desde",
               label_fin="✅ Registro de desarrollo finalizado.")
    mostrar_historial("dev_app", "📜 Historial de desarrollo")

with tab2:
    st.subheader("🌧️ Registro de mojadas por lluvia")
    cronometro("mojada_lluvia",
               label_inicio="💦 Te mojaste desde",
               label_fin="☂️ Registro de mojada finalizado.")
    mostrar_historial("mojada_lluvia", "📜 Historial de mojadas")

# DEBUG
st.divider()
st.write("Última tecla detectada:", key)
