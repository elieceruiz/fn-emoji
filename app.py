import streamlit as st

st.set_page_config(page_title="Toggle Emoji", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Botón invisible que cambia el toggle
if st.button("toggle_button", key="hidden_toggle", help="Oculto"):
    st.session_state.toggle = not st.session_state.toggle
    st.rerun()

# Inyectar JS para presionar el botón cuando se detecta una tecla
st.components.v1.html("""
<script>
document.addEventListener("keydown", function(event) {
    if (event.key === "Shift" || event.key === "Delete") {
        // Buscar el botón por su texto o atributo
        const btn = window.parent.document.querySelector('button[kind="secondary"][title="Oculto"]');
        if (btn) { btn.click(); }
    }
});
</script>
""", height=0)

# Mostrar emoji según estado
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")