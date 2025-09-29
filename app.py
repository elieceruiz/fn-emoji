# app_toggle_supr.py
import streamlit as st

st.set_page_config(page_title="Toggle Emoji", layout="centered")

# Inicializar toggle en session_state
if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Inyectar JS para detectar tecla Suprimir/Delete
st.components.v1.html("""
<script>
document.addEventListener("keydown", function(event) {
    if (event.code === "Delete" || event.key === "Delete") {
        const url = new URL(window.location.href);
        // usamos timestamp para evitar cache
        url.searchParams.set("toggle_event", Date.now());
        window.location.href = url.toString();
    }
});
</script>
""", height=0)

# Detectar param de evento
if "toggle_event" in st.query_params:
    st.session_state.toggle = not st.session_state.toggle

    # limpiar los params (ya soportado en 1.50+)
    st.query_params.clear()

    # relanzar ciclo
    st.rerun()

# Mostrar emoji según estado
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")