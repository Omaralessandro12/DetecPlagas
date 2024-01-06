User
import streamlit as st

st.set_page_config(
    page_title="Presentación de la App",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Bienvenido a la Aplicación de Detección de Plagas")
st.write("Esta aplicación ayuda en la detección de insectos y ácaros en la agricultura mexicana.")

# URL de tu aplicación en Streamlit Sharing
app_url = "https://detecplagas-cnprexgkchgbie2kpjkknh.streamlit.app/"

if st.button("Ir a la Aplicación"):
    st.markdown(f'[Abrir la Aplicación]({app_url})')  
