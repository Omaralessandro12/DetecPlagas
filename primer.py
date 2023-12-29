# presentacion_app.py

import streamlit as st

st.set_page_config(
    page_title="Presentación de la App",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Bienvenido a la Aplicación de Detección de Plagas")
st.write("Esta aplicación ayuda en la detección de insectos y ácaros en la agricultura mexicana.")

# Enlace a tu repositorio de GitHub
github_repo_url = "https://github.com/tu_usuario/tu_repositorio"

if st.button("Ir a la Aplicación en GitHub"):
    st.markdown(f'[Abrir la Aplicación en GitHub]({github_repo_url}/blob/main/APP.py)')
