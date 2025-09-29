import streamlit as st

st.set_page_config(page_title="Toggle con tecla", layout="centered")

# Estado inicial
if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Botón que cambia estado
if st.button("🔀 Cambiar estado", key="toggle_button"):
    st.session_state.toggle = not st.session_state.toggle
    st.rerun()

# Mostrar estado
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")

# Inyectar JS que hace click en el botón al presionar Enter
st.components.v1.html("""
<script>
document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        console.log("Enter detectado, simulando click en botón...");
        const boton = window.parent.document.querySelector('button[kind="secondary"]');
        if (boton) boton.click();
    }
});
</script>
""", height=0)