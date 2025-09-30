# app.py
import streamlit as st
from my_key_listener import my_key_listener

st.set_page_config(page_title="Toggle con tecla", layout="centered")

# ========================
# ESTADOS
# ========================
if "toggle" not in st.session_state:
    st.session_state.toggle = True  # estado inicial = feliz

# ========================
# FUNCIONES
# ========================
def on_button_click():
    st.session_state.toggle = not st.session_state.toggle

# ========================
# DETECTOR TECLA
# ========================
key = my_key_listener(key="listener")

if key == "Shift":
    on_button_click()

# ========================
# FRONTEND (sin CSS)
# ========================

st.title("🎛️ Control con tecla")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    # Botón visible
    st.button("Cambiar emoji", on_click=on_button_click)

st.divider()

# Mostrar emoji grande
emoji = "😊" if st.session_state.toggle else "😢"
st.header(f"{emoji} Estado actual")

st.divider()

st.subheader("⌨️ Última tecla detectada:")
st.info(f" {key if key else 'Ninguna todavía...'} ")
