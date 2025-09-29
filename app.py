import streamlit as st

st.set_page_config(page_title="Tecla activa botón", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Botón que alterna el estado
if st.button("Cambiar estado"):
    st.session_state.toggle = not st.session_state.toggle

# Mostrar emoji
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")

# --- JavaScript: detectar tecla y simular clic en el botón ---
st.markdown("""
<script>
document.addEventListener("keydown", function(event) {
    // Cambia aquí la tecla que quieras (ej: "Enter", "Shift", "Delete")
    if (event.key === "Enter") {
        const boton = window.parent.document.querySelector('button');
        if (boton) boton.click();
    }
});
</script>
""", unsafe_allow_html=True)