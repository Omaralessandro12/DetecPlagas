# Python In-built packages
from pathlib import Path
import PIL

# External packages
import streamlit as st

# Local Modules
import settings
import helper

# Setting page layout
st.set_page_config(
    page_title="Deteccion de Plagas en la agricultura Mexicana",
    # page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Sidebar
st.sidebar.header("Configuración del modelo de aprendizaje automático")

# Model Options
model_types_available = ['Deteccion', 'OtraTarea', 'OtraTarea2']  # Agrega más tareas según sea necesario
model_type = st.sidebar.multiselect("Seleccionar tarea", model_types_available, default=['Deteccion'])



#model_type = st.sidebar.radio(
#    "Seleccionar tarea", ['Deteccion' ])


confidence = float(st.sidebar.slider(
    "Seleccione la confianza del modelo", 25, 100, 40)) / 100


if not model_type:
    model_type = ['Deteccion']

selected_task = model_type[0]

if selected_task == 'Deteccion':
    model_path = Path(settings.DETECTION_MODEL)

# Selecting Detection Or Segmentation
#if model_type == 'Deteccion':
#   model_path = Path(settings.DETECTION_MODEL)
#elif model_type == 'Segmentation':
#    model_path = Path(settings.SEGMENTATION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Imagen/Config")
source_radio = st.sidebar.radio(
    "Seleccione Fuente", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Elige una imagen...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Imagen Cargada",
                         use_column_width=True)
        except Exception as ex:
            st.error("Se produjo un error al abrir la imagen.")
            st.error(ex)

    with col2:        
            if st.sidebar.button('Detectar Objeto'):
                res = model.predict(uploaded_image,
                                    conf=confidence
                                    )
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)
                try:
                    with st.expander("Resultados de la detección"):
                        for box in boxes:
                            st.write(box.data)
                except Exception as ex:
                    # st.write(ex)
                    st.write("No image is uploaded yet!")

#elif source_radio == settings.VIDEO:
#    helper.play_stored_video(confidence, model)

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)

#elif source_radio == settings.YOUTUBE:
#   helper.play_youtube_video(confidence, model)

else:
    st.error("Please select a valid source type!")
