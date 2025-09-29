# app.py
import streamlit as st

st.set_page_config(page_title="Toggle Emoji", layout="centered")

# Inicializar toggle en session_state
if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Inyectar JS para detectar F1 (simulando Fn, ya que Fn no se detecta en JS)
st.components.v1.html("""
<script>
document.addEventListener("keydown", function(event) {
    if (event.code === "F1") {
        const url = new URL(window.location.href);
        url.searchParams.set("toggle", "1");
        window.location.href = url.toString();
    }
});
</script>
""", height=0)

# Detectar si se presionó F1 mediante query param
if "toggle" in st.query_params:
    st.session_state.toggle = not st.session_state.toggle
    st.query_params.clear()  # limpia los params para no reinvertir el toggle
    st.rerun()               # rerun estable

# Mostrar emoji según estado
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")
