import streamlit as st
import webbrowser

st.set_page_config(
    page_title="Presentación de la App",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Bienvenido a la Aplicación de Detección de Plagas")
st.write("Esta aplicación ayuda en la detección de insectos y ácaros en la agricultura mexicana.")

# Enlace a tu aplicación
app_url = "https://github.com/Omaralessandro12/DetecPlagas.git/APP.py"  # Reemplaza con la URL correcta de tu aplicación

if st.button("Ir a la Aplicación"):
    webbrowser.open(app_url)

