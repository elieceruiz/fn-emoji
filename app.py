# key_button.py
import streamlit as st

st.set_page_config(page_title="Key Button", layout="centered")

if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Inyectamos JS: simula un clic en el botón oculto al presionar tecla
st.components.v1.html("""
<script>
document.addEventListener("keydown", function(event) {
    if (event.key === "Shift") {  // puedes cambiar "Shift" por "Delete", "Enter", etc
        const btn = window.parent.document.querySelector("button[data-testid='key-btn']");
        if (btn) btn.click();
    }
});
</script>
""", height=0)

# Botón oculto (se activa desde JS)
if st.button("Key Button", key="key-btn"):
    st.session_state.toggle = not st.session_state.toggle
    st.rerun()

# Mostrar estado con emoji
st.markdown("### 🟢" if st.session_state.toggle else "### 🔴")