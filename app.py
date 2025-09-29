import streamlit as st
import time

st.set_page_config(page_title="Toggle Emoji", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False
if "last_key" not in st.session_state:
    st.session_state.last_key = {}

# Botón visible de debug
if st.button("Cambiar estado", key="visible_toggle"):
    st.session_state.toggle = not st.session_state.toggle
    st.rerun()

# Inyectar JS con debug
st.components.v1.html(f"""
<script>
document.addEventListener("keydown", function(event) {{
    const debugData = {{
        key: event.key,
        code: event.code,
        time: Date.now()
    }};
    console.log("DEBUG:", debugData);

    // Mandar los datos a Streamlit usando query params
    const url = new URL(window.location.href);
    url.searchParams.set("key_pressed", JSON.stringify(debugData));
    window.location.href = url.toString();
}});
</script>
""", height=0)

# Captura desde query params
if "key_pressed" in st.query_params:
    try:
        import json
        data = json.loads(st.query_params["key_pressed"])
        st.session_state.last_key = data
    except Exception as e:
        st.session_state.last_key = {"error": str(e)}
    st.query_params.clear()
    st.rerun()

# Mostrar estado + debug
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")
st.subheader("Última tecla detectada (debug)")
st.json(st.session_state.last_key)