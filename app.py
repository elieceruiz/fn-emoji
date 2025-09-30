# app.py
import streamlit as st
from my_key_listener import my_key_listener
import time

st.set_page_config(page_title="Toggle con tecla", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = True

if "active_feedback" not in st.session_state:
    st.session_state.active_feedback = False

def on_button_click():
    st.session_state.toggle = not st.session_state.toggle
    st.session_state.active_feedback = True

key = my_key_listener(key="listener")

if key == "Shift":
    on_button_click()

emoji = "😊" if st.session_state.toggle else "😢"
st.markdown(f"### {emoji}")

if st.session_state.active_feedback:
    st.write("✨ Botón activado con Shift! ✨")
    # Reset feedback after a small delay
    time.sleep(0.3)
    st.session_state.active_feedback = False

st.write("Última tecla detectada:", key)
