import streamlit as st

st.set_page_config(page_title="ENTER universal", layout="centered")

# Estado inicial
if "toggle" not in st.session_state:
    st.session_state.toggle = False

# Input (no importa si escribes o no)
entrada = st.text_input("Escribe algo y presiona ENTER:")

# Botón oculto que será disparado por JS
if st.button("Acción", key="accion"):
    st.session_state.toggle = not st.session_state.toggle

# Mostrar estado con emoji
if st.session_state.toggle:
    st.markdown("😃 **Activo**")
else:
    st.markdown("😴 **Inactivo**")

st.json({
    "valor_capturado": entrada,
    "toggle_actual": st.session_state.toggle
})

# --- Hack JS: captura Enter y pulsa el botón ---
st.markdown("""
    <script>
    const input = window.parent.document.querySelector('input[type="text"]');
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const boton = window.parent.document.querySelector('button[kind="secondary"]');
            if (boton) boton.click();
        }
    });
    </script>
""", unsafe_allow_html=True)