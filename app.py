# key_test.py
import streamlit as st

st.set_page_config(page_title="Key Test", layout="centered")

# Guardamos la última tecla
if "last_key" not in st.session_state:
    st.session_state.last_key = "Ninguna"

st.markdown(f"### Última tecla detectada: `{st.session_state.last_key}`")

# Inyectamos JS
st.components.v1.html("""
<script>
document.addEventListener("keydown", function(event) {
    const url = new URL(window.location.href);
    url.searchParams.set("last_key", event.key); // pasamos la tecla
    window.location.href = url.toString();
});
</script>
""", height=0)

# Detectar si hay param
if "last_key" in st.query_params:
    st.session_state.last_key = st.query_params["last_key"]

    # limpiar para evitar bucle
    st.query_params.clear()

    # relanzar
    st.rerun()