# key_alert_test.py
import streamlit as st

st.set_page_config(page_title="Key Alert Test", layout="centered")

st.markdown("## Presiona cualquier tecla en la ventana 👇")

st.components.v1.html("""
<script>
document.addEventListener("keydown", function(event) {
    alert("Tecla detectada: " + event.key);
});
</script>
""", height=200)