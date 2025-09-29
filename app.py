# app_detect_key.py
import streamlit as st

st.set_page_config(page_title="Detect Tecla", layout="centered")
st.write("Presioná la tecla Suprimir y veremos qué detecta JS")

st.components.v1.html("""
<script>
document.addEventListener("keydown", function(event) {
    const div = document.getElementById("output");
    div.innerText = "event.code: " + event.code + " | event.key: " + event.key;
});
</script>
<div id="output" style="font-size:30px; margin-top:20px;">---</div>
""", height=100)