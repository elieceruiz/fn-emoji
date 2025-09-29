# app_toggle_key.py
import streamlit as st

st.set_page_config(page_title="Toggle Emoji", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False

def flip_toggle():
    st.session_state.toggle = not st.session_state.toggle

# Botón oculto
btn = st.button("hidden_btn", on_click=flip_toggle)

# JS que simula click al presionar Shift
st.components.v1.html("""
<script>
document.addEventListener("keydown", function(event) {
    if (event.key === "Shift") {
        const btn = window.parent.document.querySelector('button[kind="secondary"]'); 
        if (btn && btn.innerText === "hidden_btn") {
            btn.click();
        }
    }
});
</script>
""", height=0)

st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")