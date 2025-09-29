# app_toggle_supr.py
import streamlit as st

st.set_page_config(page_title="Toggle Emoji", layout="centered")

# Inicializar toggle en session_state
if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Inyectar JS para detectar tecla Suprimir en español y estándar
st.components.v1.html("""
<script>
document.addEventListener("keydown", function(event) {
    // Detecta Delete (inglés) o Supr (español)
    if (event.code === "Delete" || event.key === "Delete") {
        const url = new URL(window.location.href);
        url.searchParams.set("toggle", "1");
        window.location.href = url.toString();
    }
});
</script>
""", height=0)

# Detectar si se presionó Suprimir mediante query param
if "toggle" in st.query_params:
    st.session_state.toggle = not st.session_state.toggle
    st.query_params.clear()  # limpia params para no reinvertir al recargar
    st.rerun()               # rerun estable

# Mostrar emoji según estado
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")