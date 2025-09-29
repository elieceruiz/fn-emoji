import streamlit as st

st.set_page_config(page_title="Toggle con tecla", layout="centered")

# Estado inicial
if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Leer query param
query_params = st.query_params

if "toggle" in query_params:
    st.session_state.toggle = not st.session_state.toggle
    st.query_params.clear()
    st.rerun()

# Mostrar estado
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")

# DEBUG en pantalla
st.write("Query params actuales:", dict(query_params))

# Inyectar JS
st.components.v1.html("""
<script>
document.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        console.log("ENTER detectado!");   // <-- DEBUG en consola
        const url = new URL(window.location.href);
        url.searchParams.set("toggle", "1");
        console.log("Nueva URL:", url.toString());  // <-- DEBUG en consola
        window.location.href = url.toString();
    }
});
</script>
""", height=0)