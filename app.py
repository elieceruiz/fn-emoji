# app.py
# app_toggle_delete.py
import streamlit as st

st.set_page_config(page_title="Toggle Emoji", layout="centered")

# Inicializar toggle en session_state
if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Inyectar JS para detectar tecla Suprimir (Delete)
st.components.v1.html("""
<script>
document.addEventListener("keydown", function(event) {
    if (event.code === "Delete") {  // tecla Suprimir
        const url = new URL(window.location.href);
        url.searchParams.set("toggle", "1");
        window.location.href = url.toString();
    }
});
</script>
""", height=0)

# Detectar si se presionó Delete mediante query param
if "toggle" in st.query_params:
    st.session_state.toggle = not st.session_state.toggle
    st.query_params.clear()  # limpiar para no reinvertir al recargar
    st.rerun()               # rerun estable

# Mostrar emoji según estado
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")