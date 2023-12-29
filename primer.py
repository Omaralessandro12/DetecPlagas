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
github_repo_url = "https://github.com/Omaralessandro12/DetecPlagas.git"

if st.button("Ir a la Aplicación en GitHub"):
    st.markdown(f'[Abrir la Aplicación en GitHub]({github_repo_url}BreadcrumbsDetecPlagas/APP.py)')
