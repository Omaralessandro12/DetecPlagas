# Paquetes integrados de Python
from pathlib import Path
import PIL

# Paquetes externos
import streamlit as st

# Módulos locales
import settings
import helper

# Configuracion del diseño de la página

st.set_page_config(
    page_title="Deteccion de Plagas en la agricultura Mexicana",
    # page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Detección de Plagas en la agricultura Mexicana")
st.write ("APLICACIÓN PARA LA DETECCIÓN DE INSECTOS E ACAROS EN LA AGRICULTURA MEXICANA ")


# Sidebar
st.sidebar.header("Configuración del modelo de aprendizaje automático")

# Opciones de Modelos 
model_types_available = ['Yolov8', 'Resnet50']  # Agrega más tareas según sea necesario
model_type = st.sidebar.multiselect("Seleccionar tarea", model_types_available, default=['Yolov8'])

if not model_type:
    model_type = ['Yolov8']

selected_task = model_type[0]

if selected_task == 'Yolov8':
    model_path = Path(settings.DETECTION_MODEL)

# Cargar modelo ML previamente entrenado
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"No se puede cargar el modelo. Verifique la ruta especificada: {model_path}")
    st.error(ex)

source_radio = st.sidebar.radio(
    "Seleccione Fuente", settings.LISTA_FUENTES)

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
            if st.sidebar.button('Detectar Plaga'):
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

else:
    st.error("Please select a valid source type!")
