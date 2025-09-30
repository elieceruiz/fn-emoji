# app.py
import streamlit as st
from my_key_listener import my_key_listener

st.set_page_config(page_title="Toggle con tecla", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = True  # estado inicial = feliz

def on_button_click():
    st.session_state.toggle = not st.session_state.toggle

key = my_key_listener(key="listener")

if key == "Shift":
    on_button_click()

button_clicked = st.button("Cambiar emoji", on_click=on_button_click)

emoji = "😊" if st.session_state.toggle else "😢"
st.markdown(f"### {emoji}")
st.write("Última tecla detectada:", key)
