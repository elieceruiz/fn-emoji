import streamlit as st

st.set_page_config(page_title="Toggle con tecla", layout="centered")

# Estado inicial
if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Leer query param (para comunicación con JS)
query_params = st.query_params

if "toggle" in query_params:
    st.session_state.toggle = not st.session_state.toggle
    st.query_params.clear()
    st.rerun()

# Mostrar estado
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")

# Inyectar JS que escucha la tecla y mete un param en la URL
st.components.v1.html("""
<script>
document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        const url = new URL(window.location.href);
        url.searchParams.set("toggle", "1");
        window.history.pushState({}, "", url);  // Actualiza sin redirigir
        location.reload();  // Recarga para que Streamlit lo lea
    }
});
</script>
""", height=0)