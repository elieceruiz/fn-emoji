import streamlit as st

st.set_page_config(page_title="Debug tecla", layout="centered")

# Slot para guardar última tecla
if "last_key" not in st.session_state:
    st.session_state.last_key = "ninguna"

st.write("Última tecla detectada:", st.session_state.last_key)

# Inyectar JS con Streamlit.setComponentValue
st.components.v1.html("""
<script>
document.addEventListener("keydown", function(event) {
    const tecla = event.key;
    console.log("Tecla detectada:", tecla);
    // Enviar valor a Streamlit por postMessage
    window.parent.postMessage({isStreamlitMessage: true, type: "streamlit:setComponentValue", value: tecla}, "*");
});
</script>
""", height=0)

# Mostrar debug de mensajes recibidos
st.json(st.session_state)