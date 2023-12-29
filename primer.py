# presentacion_app.py

import streamlit as st

st.set_page_config(
    page_title="Presentación de la App",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Bienvenido a la Aplicación de Detección de Plagas")
st.write("Esta aplicación ayuda en la detección de insectos y ácaros en la agricultura mexicana.")

if st.button("Ir a la Aplicación"):
    st.markdown('<a href="APP.py" target="_blank">Abrir la Aplicación</a>', unsafe_allow_html=True)
