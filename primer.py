import streamlit as st

st.set_page_config(
    page_title="Presentación de la App",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Bienvenido a la Aplicación de Detección de Plagas")
st.write("Esta aplicación ayuda en la detección de insectos y ácaros en la agricultura mexicana.")

# URL de App.py
app_url = "https://detecplagas-cnprexgkchgbie2kpjkknh.streamlit.app/"

#validar javascript para abrir pagina ahi mismo 
if st.button("Ir a la Aplicación"):
    st.markdown(f'[Abrir la Aplicación]({app_url})')  
