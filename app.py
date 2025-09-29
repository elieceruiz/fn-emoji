import streamlit as st

st.set_page_config(page_title="Key Event", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False

event = st.key_event("Press a key")

if event.key == "Delete" or event.key == "Shift":
    st.session_state.toggle = not st.session_state.toggle
    st.rerun()

st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")